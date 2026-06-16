from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404

from .models import Habit,HabitLog,HabitCategory,profile
from .forms import SignupForm,LoginForm,AddHabitForm,categoryForm,profileForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from datetime import date,timedelta


def signup(request):

    if request.method=='POST':

        form=SignupForm(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
        
            user.save()
            return redirect('login')

    form=SignupForm()

    return render(request,'signup.html',{'form':form})




def Login(request):

    if request.method=='POST':

        form=LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user=authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('home')

            else:
                messages.error(request,"user does not exist")
                return redirect('login')
            
        else:
            messages.error(request,"Invalid password or username")
     
    else:
        form=LoginForm()


    return render(request,'login.html',{'form':form})





def logout_view(request):

    logout(request)

    return redirect('login')




@login_required
def add_habit(request):

    if request.method=='POST':
        form=AddHabitForm(request.POST)

        
        #creating dropdown
        form.fields['category'].queryset=(HabitCategory.objects.filter(user=request.user))


        if form.is_valid():
            habit=form.save(commit=False)
            habit.user=request.user

            habit.save()

            return redirect('home')
        
        else:
            messages.error(request,"Enter correct habit name")
    
    else:

        form=AddHabitForm()
        
        #creating dropdown
        form.fields['category'].queryset=(HabitCategory.objects.filter(user=request.user))

    return render(request,'add.html',{'form':form})





@login_required
def add_category(request):

    if request.method=='POST':

        form=categoryForm(request.POST)

        if form.is_valid():
            category=form.save(commit=False)
            category.user=request.user

            category.save()

            return redirect('home')
        
        else:

            messages.error(request,"Enter valid category name")
    else:
        form=categoryForm()

    return render(request,'category.html',{'form':form})



def category_list(request):
    categories=HabitCategory.objects.filter(user=request.user)

    return render(request,'categorylist.html',{'categories':categories})

def delete_category(request,id):
    category=HabitCategory.objects.get(user=request.user,id=id)

    category.delete()

    return redirect('category')


def update_category(request,id):
    category=HabitCategory.objects.get(user=request.user,id=id)

    if request.method=='POST':
        form=categoryForm(request.POST,instance=category)

        if form.is_valid():
            form.save()

        else:
            messages.error(request,"Enter valid category name")
    else:
        form=categoryForm(instance=category)
    
    return render(request,'category.html',{"form":form})





@login_required
def update_habit(request,id):
      
    habit=get_object_or_404(Habit,id=id,user=request.user)

    if request.method=="POST":

        form=AddHabitForm(request.POST,instance=habit)

        if form.is_valid():
            form.save()
            return redirect('home')
        
        else:
            messages.error(request,"Enter valid name")
    else:

        form=AddHabitForm(instance=habit)
     
    return render(request,'add.html',{'form':form})




@login_required
def delete_habit(request,id):
    habit=Habit.objects.get(id=id,user=request.user)

    habit.delete()

    return redirect('home')

@login_required
def completion(request,id):
    habit=get_object_or_404(Habit,id=id,user=request.user)

    log,created=HabitLog.objects.get_or_create(habit=habit,logdate=date.today(),completion=True)

    log.save()

    return redirect('home')
      



@login_required
def home(request):

    category_id=request.GET.get("category")

    habits=Habit.objects.filter(user=request.user)

    search = request.GET.get('search')

    if search:
        habits=habits.filter(title__icontains=search)

    if category_id:
        habits=habits.filter(category=category_id)

    categories=HabitCategory.objects.filter(user=request.user)

    habit_lst=[]
    todaydate=date.today()

    longest_streak=0

    for habit in habits:
        completed=HabitLog.objects.filter(habit=habit,completion=True,logdate=date.today()).exists()

        streak=streak_count(habit)

        if streak>habit.max_streak:
            habit.max_streak=streak
            habit.save()
    
        habit_lst.append({
            'habit':habit,
            'completed':completed,
            'streak':streak,
            'max_streak':habit.max_streak   
        })

    total_habits=habits.count()

    total_completion=HabitLog.objects.filter(habit__user=request.user,completion=True).count()

    completed_today=0
    
    for habit in habits:
        if HabitLog.objects.filter(habit=habit,completion=True,logdate=date.today()).exists():
            completed_today+=1

    if total_habits > 0:
        progress = (completed_today / total_habits) * 100

    else:
        progress = 0

    pending=total_habits-completed_today

    username=request.user.username

    context={'total_completion':total_completion,'pending':pending,'habits':habit_lst,'username':username,'progress':round(progress),'total_habits':total_habits,'completed_today':completed_today,"categories":categories}


    return render(request,'home.html',context)






def streak_count(habit):

    streak=0
    current_date=date.today()

    while True:
        completed=HabitLog.objects.filter(habit=habit,completion=True,logdate=current_date).exists()
        
        if completed:
            streak+=1
            current_date-=timedelta(days=1)
        else:
            break

    return streak




@login_required
def history(request,id):
    habit=get_object_or_404(Habit,id=id,user=request.user)

    habit_history=HabitLog.objects.filter(habit=habit).order_by('-logdate')

    context={'habit_history':habit_history}

    return render(request,'history.html',context)




@login_required
def report(request):

    today=date.today()

    montly_count=HabitLog.objects.filter(completion=True,logdate__month=today.month,logdate__year=today.year,habit__user=request.user).count()

    habits=Habit.objects.filter(user=request.user)

    habitCount=[]

    for habit in habits:
        habit_count=HabitLog.objects.filter(habit=habit,completion=True).count()

        habitCount.append({"habit": habit,"count": habit_count})

    context={ 'total_habits': habits.count(),'montly_count':montly_count,'habitCount':habitCount}

    return render(request,'report.html',context)

def profile_view(request):
    name,created=profile.objects.get_or_create(user=request.user)
    
    if request.method=='POST':
        form=profileForm(request.POST,request.FILES,instance=name)

        if form.is_valid():
            form.save()

            return redirect('home')
    
    else:
        form=profileForm(instance=name)
    
    return render(request,'profile.html',{'form':form})


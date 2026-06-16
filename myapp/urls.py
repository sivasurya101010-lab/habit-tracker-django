from django.urls import path
from .import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('login/',views.Login,name='login'),
    path('add/',views.add_habit,name='add'),
    path('',views.home,name='home'),
    path('logout/',views.logout_view,name='logout'),
    path('update/<int:id>',views.update_habit,name='update'),
    path('delete/<int:id>/',views.delete_habit,name='delete'),
    path('completed/<int:id>/',views.completion,name='completed'),
    path('history/<int:id>/',views.history,name='history'),
    path('category/',views.add_category,name='category'),
    path('categories/',views.category_list,name='category_list'),
    path('category/update/<int:id>/',views.update_category,name='update_category'),
    path('category/delete/<int:id>/',views.delete_category,name='delete_category'),
    path('report/',views.report,name='report'),
    path('profile/',views.profile_view,name='profile'),

]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.loginPage, name='login'),
    path('admin/logout/', views.logoutPage, name='logout'),
    path('accounts/register/', views.registerPage, name='register'),
    path('profile/leader/<username>/', views.familyLeader, name='family_leader'),
    path('profile/leader/<username>/family', views.create_family, name='create_family'),
    path('profile/leader/<username>/chores', views.create_chore, name='create_chore'),
]

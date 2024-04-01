from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/login/', views.loginPage, name='login'),
    path('accounts/register/', views.registerPage, name='register'),
    path('admin/logout/', views.logoutPage, name='logout'),
    path('profile/leader/<username>/', views.familyLeader, name='family_leader'),
]

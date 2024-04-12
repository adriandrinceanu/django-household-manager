from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.loginPage, name='login'),
    path('admin/logout/', views.logoutPage, name='logout'),
    path('accounts/register/', views.registerPage, name='register'),
    path('profile/leader/<str:username>/', views.familyLeader, name='family_leader'),
    path('profile/leader/<str:username>/family', views.create_family, name='create_family'),
    path('profile/leader/<str:username>/chores', views.create_chore_view, name='create_chore'),
    path('profile/leader/<str:username>/<int:chore_id>/chores/delete', views.delete_chore_view, name='delete_chore'),
    path('profile/leader/<str:username>/budgets', views.budget_view, name='budgets'),
    path('profile/leader/<str:username>/add_budgets', views.add_budget, name='add_budget'),
    path('profile/leader/<str:username>/add_monthly_budgets', views.add_monthly_budget, name='add_monthly_budget'),
    path('profile/leader/<str:username>/delete_monthly_budget/<int:budget_id>/', views.delete_monthly_budget, name='delete_monthly_budget'),
    path('profile/leader/<str:username>/delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),
    path('profile/leader/<str:username>/expenses/', views.expense_view, name='expenses'),
    path('profile/leader/<str:username>/add_expenses/', views.add_expense, name='add_expense'),
    path('profile/leader/<str:username>/delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]


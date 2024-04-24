from django.urls import path
from . import views

urlpatterns = [
    path('/<str:username>/', views.index, name='index'),
    path('accounts/login/', views.loginPage, name='login'),
    path('admin/logout/', views.logoutPage, name='logout'),
    path('accounts/register/', views.registerPage, name='register'),
    path('profile/leader/<str:username>/', views.familyLeader, name='family_leader'),
    path('profile/leader/<str:username>/family', views.create_family, name='create_family'),
    path('profile/leader/<str:username>/<int:member_id>/member/delete', views.delete_member, name='delete_member'),
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
    path('profile/member/<str:username>/', views.familyMember, name='family_member'),
    path('profile/member/<str:username>/chores', views.chore_view, name='chore_view'),
    path('chore_done/<int:chore_id>/', views.chore_done, name='chore_done'),
    path('profile/member/<str:username>/view_budgets', views.budget_view, name='view_budgets'),
    path('profile/member/<str:username>/expenses', views.expense_view, name='member_expenses'),
    path('profile/family_member/<str:username>/chat', views.family_room_view, name='chat'),
    path('unread_messages_count/', views.get_unread_messages_count, name='unread_messages_count'),
    path('mark_messages_as_read/', views.mark_messages_as_read, name='mark_messages_as_read'),
    path('expenses_count/<str:username>/', views.get_family_expenses_counter, name='expenses_count'),
    path('mark_expenses_as_read/<str:username>/', views.mark_expenses_as_read, name='mark_expenses_as_read'),
    # path('expenses_view/<str:username>', views.get_family_expenses, name='expenses_view'),

]


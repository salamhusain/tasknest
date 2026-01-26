from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('task/create/', views.task_create_view, name='task_create'),
    path('task/<int:pk>/', views.task_detail_view, name='task_detail'),
    path('task/<int:pk>/update/', views.task_update_view, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete_view, name='task_delete'),
    path('task/<int:pk>/complete/', views.task_complete_view, name='task_complete'),
]

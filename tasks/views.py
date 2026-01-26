from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Task
from .forms import TaskForm, UserRegisterForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('tasks:dashboard')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('tasks:dashboard')
    else:
        form = UserRegisterForm()
    
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('tasks:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('tasks:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('tasks:login')

@login_required
def dashboard_view(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    tasks = Task.objects.filter(user=request.user)
    
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    context = {
        'tasks': tasks,
        'total_tasks': Task.objects.filter(user=request.user).count(),
        'pending_tasks': Task.objects.filter(user=request.user, status='pending').count(),
        'completed_tasks': Task.objects.filter(user=request.user, status='completed').count(),
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    
    return render(request, 'tasks/dashboard.html', context)

@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('tasks:dashboard')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks:dashboard')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update', 'task': task})

@login_required
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('tasks:dashboard')
    
    return render(request, 'tasks/task_detail.html', {'task': task, 'delete_mode': True})

@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_complete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.mark_completed()
    messages.success(request, 'Task marked as completed!')
    return redirect('tasks:dashboard')

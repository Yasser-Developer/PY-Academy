from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm  # این خط باید باشه
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    # XP تا سطح بعدی (هر سطح ۱۰۰ XP بیشتر از قبلی)
    xp_needed_for_current = request.user.level * 100
    xp_needed_for_next = (request.user.level + 1) * 100
    xp_to_next = xp_needed_for_next - request.user.xp
    progress = (request.user.xp / xp_needed_for_current * 100) if xp_needed_for_current > 0 else 0

    context = {
        'user': request.user,
        'xp': request.user.xp,
        'level': request.user.level,
        'is_vip': request.user.is_vip,
        'xp_to_next': max(xp_to_next, 0),
        'progress': min(progress, 100),
        'register_date': request.user.date_joined.strftime("%Y/%m/%d") if request.user.date_joined else "نامشخص",
        'email': request.user.email or "تنظیم نشده",
        'phone': request.user.phone or "تنظیم نشده",
    }
    return render(request, 'accounts/dashboard.html', context)


def leaderboard(request):
    top_users = CustomUser.objects.order_by('-xp', 'username')[:10]
    return render(request, 'accounts/leaderboard.html', {'top_users': top_users})


def learning_path(request):
    return render(request, 'accounts/learning_path.html')
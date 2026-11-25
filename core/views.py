from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages as flash
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import RegisterForm, LoginForm, MessageForm
from django.contrib.auth.decorators import login_required


def register_view(request):
    """Регистрация пользователя."""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:register_success')
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})


def register_success_view(request):
    """Страница успешной регистрации."""
    return render(request, 'core/register_success.html')


def login_view(request):
    """Авторизация пользователя."""
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('core:home')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    """Выход из системы."""
    logout(request)
    return redirect('core:login')


def home_view(request):
    """Главная страница (куда редиректим после логина)."""
    return render(request, 'core/home.html')


def message_view(request):
    """Отправка сообщения (обычный POST, без Ajax)."""
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.save()
            flash.success(request, 'Сообщение успешно отправлено!')
            return redirect('core:message')
    else:
        form = MessageForm()

    return render(request, 'core/message.html', {'form': form})


@require_POST
def message_ajax_view(request):
    """Отправка сообщения через Ajax. Возвращает JSON."""
    form = MessageForm(request.POST)
    if form.is_valid():
        msg = form.save(commit=False)
        if request.user.is_authenticated:
            msg.user = request.user
        msg.save()
        return JsonResponse({'ok': True, 'message': 'Сообщение успешно отправлено!'})

    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

@login_required
def profile_view(request):
    """Профиль пользователя: данные + его сообщения."""
    if not request.user.is_authenticated:
        return redirect('core:login')

    user_messages = request.user.messages.all()
    return render(request, 'core/profile.html', {
        'user_obj': request.user,
        'messages_list': user_messages,
    })
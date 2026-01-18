from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.views import View
from django.utils.decorators import method_decorator
from .models import MyUser, UserProfile, UserBlendInteraction
from .forms import (UserRegistrationForm, UserLoginForm, UserProfileForm)
from main_functionality.models import Blend


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        
        form = UserRegistrationForm()
        next_url = request.GET.get('next', '/accounts/profile/')
        return render(request, 'accounts/register.html', {
            'form': form,
            'next_url': next_url
        })
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                    login(request, user)

                    next_url = request.POST.get('next_url') or request.GET.get('next') or '/accounts/profile/'
                    return redirect(next_url)
                    
            except Exception as e:
               form.add_error(None, f'Ошибка при регистрации: {str(e)}')
        else:
            form.add_error(None, 'Пожалуйста, исправьте ошибки в форме.')
        
        next_url = request.POST.get('next_url', '/accounts/profile/')
        return render(request, 'accounts/register.html', {
            'form': form,
            'next_url': next_url
        })


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        
        form = UserLoginForm()
        next_url = request.GET.get('next', '/accounts/profile/')
        return render(request, 'accounts/login.html', {
            'form': form,
            'next_url': next_url
        })
    
    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                next_url = request.POST.get('next_url') or request.GET.get('next') or '/accounts/profile/'
                return redirect(next_url)
        
        next_url = request.POST.get('next_url', '/accounts/profile/')
        return render(request, 'accounts/login.html', {
            'form': form,
            'next_url': next_url
        })


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, _('Вы успешно вышли из системы'))
        return redirect('/')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        
        user_blends = Blend.objects.filter(
            user_interactions__user=user,
            user_interactions__created_by_user=True
        ).distinct().order_by('-created_at')
        
        saved_blends = Blend.objects.filter(
            user_interactions__user=user,
            user_interactions__saved=True
        ).distinct().order_by('-created_at')
        
        context = {
            'user': user,
            'user_blends': user_blends,
            'saved_blends': saved_blends,
        }
        
        return render(request, 'accounts/profile.html', context)


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request):
        user = request.user
        profile_form = UserProfileForm(instance=user)
        
        return render(request, 'accounts/edit.html', {
            'profile_form': profile_form,
        })
    
    def post(self, request):
        user = request.user
        profile_form = UserProfileForm(request.POST, instance=user)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _('Профиль успешно обновлен!'))
            return redirect('/accounts/profile/')
        
        return render(request, 'accounts/edit.html', {
            'profile_form': profile_form,
        })


@method_decorator(login_required, name='dispatch')
class SaveBlendView(View):
    def post(self, request, blend_id):
        blend = get_object_or_404(Blend, id=blend_id)
        
        interaction, created = UserBlendInteraction.objects.get_or_create(
            user=request.user,
            blend=blend,
            defaults={'saved': True}
        )
        
        if not created:
            interaction.saved = not interaction.saved
            interaction.save()
        
        return redirect(request.META.get('HTTP_REFERER', '/'))


@method_decorator(login_required, name='dispatch')
class RateBlendView(View):
    def post(self, request, blend_id):
        blend = get_object_or_404(Blend, id=blend_id)
        rating = request.POST.get('rating')
        
        if rating and rating.isdigit():
            rating_value = int(rating)
            
            if 1 <= rating_value <= 5:
                interaction, created = UserBlendInteraction.objects.update_or_create(
                    user=request.user,
                    blend=blend,
                    defaults={'rating': rating_value}
                )
                
                if created and hasattr(request.user, 'profile'):
                    profile = request.user.profile
                    if hasattr(profile, 'blends_rated'):
                        profile.blends_rated += 1
                        profile.save()
                
                messages.success(request, f'Вы поставили оценку {rating_value}/5')
            else:
                messages.error(request, 'Оценка должна быть от 1 до 5')
        else:
            messages.error(request, 'Пожалуйста, выберите оценку')
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
@method_decorator(login_required, name='dispatch')
class RemoveFromSavedView(View):
    def post(self, request, blend_id):
        blend = get_object_or_404(Blend, id=blend_id)
        
        interaction = UserBlendInteraction.objects.filter(
            user=request.user,
            blend=blend,
            saved=True
        ).first()
        
        if interaction:
            interaction.delete()
            messages.success(request, _('Купаж удален из вашего профиля'))
        else:
            messages.warning(request, _('Этот купаж не найден в вашем профиле'))
        
        return redirect('/accounts/profile/')

def get_user_role_display(user):
    if not user.is_authenticated:
        return 'Гость'
    return user.get_role_display()


def save_blend_to_profile(request, blend_id):
    blend = get_object_or_404(Blend, id=blend_id)
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    interaction, created = UserBlendInteraction.objects.update_or_create(
        user=request.user,
        blend=blend,
        defaults={'saved': True, 'published': False}
    )
    
    messages.success(request, 'Купаж сохранен в ваш профиль!')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def publish_blend(request, blend_id):
    blend = get_object_or_404(Blend, id=blend_id)
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    interaction, created = UserBlendInteraction.objects.update_or_create(
        user=request.user,
        blend=blend,
        defaults={'saved': True, 'published': True, 'created_by_user': True}
    )
    
    messages.success(request, 'Купаж опубликован и добавлен в каталог!')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def cancel_blend(request, blend_id):
    blend = get_object_or_404(Blend, id=blend_id)

    has_interactions = UserBlendInteraction.objects.filter(blend=blend).exists()
    
    if not has_interactions:
        blend.delete()
        messages.info(request, 'Создание купажа отменено')
    else:
        messages.info(request, 'Купаж уже был сохранен и не был удален')
    
    return redirect('/')
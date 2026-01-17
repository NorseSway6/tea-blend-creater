from django.contrib import admin
from django.urls import include, path
from main_functionality.views import *
from accounts.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('blend_creater/', tea_blend_creater_form),
    path('save/', save_blend),
    path('regenerate/', regenerate_blend),
    path('catalog/', catalog_view),
    path('blend/<int:blend_id>/', blend_detail),
    path('about/', about_view),
    path('accounts/register/', RegisterView.as_view()),
    path('accounts/login/', LoginView.as_view()),
    path('accounts/logout/', LogoutView.as_view()),
    path('accounts/profile/', ProfileView.as_view()),
    path('accounts/profile/edit/', EditProfileView.as_view()),
    path('accounts/blend/<int:blend_id>/save/', SaveBlendView.as_view()),
    path('accounts/blend/<int:blend_id>/rate/', RateBlendView.as_view()),
]
from django.contrib import admin
from django.urls import include, path
from main_functionality.views import *
from accounts.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('blend_creater/', tea_blend_creater_form),
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
    path('accounts/blend/<int:blend_id>/rate/', RateBlendView.as_view(), name='rate_blend'),
    path('remove_saved/<int:blend_id>/', RemoveFromSavedView.as_view(), name='remove_saved'),
    path('blend/save/<int:blend_id>/', save_blend_to_profile),
    path('blend/publish/<int:blend_id>/', publish_blend),
    path('blend/cancel/<int:blend_id>/', cancel_blend),
]
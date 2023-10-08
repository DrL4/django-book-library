from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('restartPassword/', auth_views.PasswordResetView.as_view(),
         name='resetPassword'),
    path('passwordResetDone/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('signup/', views.register, name='signup'),
    path('user/profile/', views.UserDetailView.as_view(), name='UserProfile'),
    path('user/profile/update', views.profile, name='UserUpdate'),
    path('user/profile/updateImage',
         views.ProfileUpdateView.as_view(), name='ProfileUpdate'),
    
    path('librarian/index', views.index, name='index'),
]

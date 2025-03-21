# urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from bit_main import viewsets

urlpatterns = [
    path('signup/', viewsets.SignUpUserViewset.as_view(), name='signup'),
    path('login/', viewsets.LoginUserViewset.as_view(), name='login'),
    path('user/update/', viewsets.UserUpdateAPIViewset.as_view(), name='update-user'),
    path('logout/', viewsets.LogoutUserViewset.as_view(), name='logout'),
    path('password-reset/', viewsets.PasswordResetRequestViewset.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', viewsets.PasswordResetConfirmViewset.as_view(), name='password-reset-confirm'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('delete-account/', viewsets.DeleteUserView.as_view(), name='delete-account'),
]

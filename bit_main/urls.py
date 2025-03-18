# urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from bit_main.viewsets import SignUpUserViewset, LoginUserViewset, UserUpdateAPIViewset, LogoutUserViewset, \
    PasswordResetRequestViewset, PasswordResetConfirmViewset

urlpatterns = [
    path('signup/', SignUpUserViewset.as_view(), name='signup'),
    path('login/', LoginUserViewset.as_view(), name='login'),
    path('user/update/', UserUpdateAPIViewset.as_view(), name='update-user'),
    path('logout/', LogoutUserViewset.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestViewset.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmViewset.as_view(), name='password-reset-confirm'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import * 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# API endpoints for user authentication
urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    #jwt authentication
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
  
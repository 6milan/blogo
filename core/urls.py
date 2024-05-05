from django.urls import path
from .views import (
    SiteSettingsDetail,
    UserLogin,
    UserLogout,
    UserRegistration,
    UserListView
)

urlpatterns = [
    # Site Settings API
    path('api/site-settings/', SiteSettingsDetail.as_view(), name='site-settings-detail'),

    # User Authentication APIs
    path('api/user/login/', UserLogin.as_view(), name='user-login'),
    path('api/user/logout/', UserLogout.as_view(), name='user-logout'),
    path('api/user/register/', UserRegistration.as_view(), name='user-registration'),
    
    # User List API
    path('api/user/list/', UserListView.as_view(), name='user-list'),
    path('auth-api/', UserLogin.as_view(), name='user-login'),
    
    # Add other URL patterns as needed
]


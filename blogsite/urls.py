from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.models import User
from blog.views import AuthenticationAPIView
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('auth-api/', AuthenticationAPIView.as_view(), name='auth-api'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_drf')),
    path('core/', include('core.urls')),
    path('custom-auth-url/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # Redirect the root path to the blog path, adjust as needed
    path('', RedirectView.as_view(url='/blog/', permanent=False)),
    
    # Include only specific DRF router URLs
    path('api/', include(router.urls)),  # Adjust the path as needed

    # Serve static and media files during development
    # (Make sure this is only active in DEBUG mode)
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
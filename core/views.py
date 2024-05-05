from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import SiteSettingsSerializer, UserSerializer
from .models import SiteSettings
from rest_framework.authtoken.models import Token
from blog.models import Post
from blog.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated  # Import IsAuthenticated
from blog.serializers import CommentSerializer
from blog.models import Comment
from rest_framework.permissions import AllowAny

class SiteSettingsDetail(generics.RetrieveUpdateAPIView):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer


class UserLogin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == 'POST':
            # Handle your authentication logic here
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'})
            else:
                return Response({'message': 'Login failed'}, status=status.HTTP_400_BAD_REQUEST)
            
class UserLogout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class UserRegistration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create a token for the newly registered user
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user_id': user.id, 'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()  # Retrieve all users
    serializer_class = UserSerializer  # Use a serializer to format the data

    def list(self, request, *args, **kwargs):
        # Custom logic can be added here if needed
        # For example, you can filter the queryset or add pagination
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

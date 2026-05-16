from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer
from .utils import ApiResponse, ResponseMessages


class RegisterView(generics.GenericAPIView):
    """Register a new hunter (user)"""
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    
    def post(self, request):
        """Handle user registration"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return ApiResponse.created(
                data={
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                message=ResponseMessages.USER_REGISTERED
            )
        return ApiResponse.validation_error(
            errors=serializer.errors,
            message=ResponseMessages.VALIDATION_ERROR
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update current user profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        """Get user profile"""
        serializer = self.get_serializer(self.get_object())
        return ApiResponse.success(
            data=serializer.data,
            message=ResponseMessages.PROFILE_RETRIEVED
        )
    
    def update(self, request, *args, **kwargs):
        """Update user profile"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(
                data=serializer.data,
                message=ResponseMessages.PROFILE_UPDATED
            )
        return ApiResponse.validation_error(
            errors=serializer.errors,
            message=ResponseMessages.VALIDATION_ERROR
        )


class LogoutView(APIView):
    """Logout user by blacklisting refresh token"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return ApiResponse.error(
                    message="Refresh token is required",
                    error_code="MISSING_TOKEN"
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return ApiResponse.success(
                message=ResponseMessages.LOGOUT_SUCCESS
            )
        except Exception as e:
            return ApiResponse.error(
                message=ResponseMessages.INVALID_TOKEN,
                error_code="INVALID_TOKEN"
            )


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Hardcoded credentials
        valid_username = "admin"
        valid_password = "admin123"
        valid_email = "admin@company.com"
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username == valid_username and password == valid_password:
            # Get or create the hardcoded admin user
            user, created = User.objects.get_or_create(
                username=valid_username,
                defaults={
                    'email': valid_email,
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True
                }
            )
            
            if created:
                user.set_password(valid_password)
                user.save()
            
            # Create or get token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'is_hr': True,
                    'is_employee': False
                }
            }, status=status.HTTP_200_OK)
        
        return Response(
            {"non_field_errors": ["Incorrect Credentials"]},
            status=status.HTTP_401_UNAUTHORIZED
        )
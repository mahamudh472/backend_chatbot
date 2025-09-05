from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail


class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        try:
            send_mail(
            subject='Verify your email',
            message='Thank you for signing up. Please verify your email address.',
            from_email='no-reply@example.com',
            recipient_list=[user.email],
            fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't fail the signup
            print(f"Email sending failed: {e}")
        return Response({
            "success": True,
            "message": "User signed up successfully",
            "user": {
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username_or_email = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=username_or_email, password=password)
        if not user:
            # Try email authentication
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

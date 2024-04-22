from rest_framework import generics 
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Models
from .models import Note
from .serializers import NoteSerializer, RegisterSerializer

# Authentication
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Register
@api_view(['POST'])
def register(request):
    data = request.data
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'User created successfully'}, status=201)
    else:
        return Response(serializer.errors, status=400)

# Login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password') 
        if username is None or password is None:
            return Response({'error': 'Please provide username and password'}, status=400)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.auth is None:
        return Response({'error': 'Not logged in'}, status=401)
    
    # Delete token
    request.user.auth_token.delete()
    return Response({ 'success': 'Logged out successfully'}, status=200)

# Notes
class NoteList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    # lookup_field = 'id'


from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer
from organisations.models import Organisation

@api_view(['POST'])
def register(request):
    data = request.data
    if User.objects.filter(email=data['email']).exists():
        return JsonResponse({'status': 'Bad request', 'message': 'Email already exists'}, status=400)
    user = User(
        firstName=data['firstName'],
        lastName=data['lastName'],
        email=data['email'],
        password=make_password(data['password']),
        phone=data.get('phone', '')
    )
    user.save()

    organisation = Organisation(name=f"{user.firstName}'s Organisation")
    organisation.save()
    organisation.users.add(user)

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        'status': 'success',
        'message': 'Registration successful',
        'data': {
            'accessToken': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
    }, status=201)

@api_view(['POST'])
def login(request):
    data = request.data
    user = authenticate(email=data['email'], password=data['password'])
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'accessToken': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
        }, status=200)
    else:
        return JsonResponse({'status': 'Bad request', 'message': 'Authentication failed'}, status=401)

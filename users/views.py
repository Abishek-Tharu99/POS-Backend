from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def signup(request):

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Check Existing Email
    if User.objects.filter(email=email).exists():
        return Response({
            'message': 'Email already exists'
        }, status=400)
        
    if User.objects.filter(username=username).exists():
        return Response({
            'message': 'Username already exists'
        }, status=400)

    # Save User
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({
        'message': 'Signup Successful'
    }, status=201)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):

    return Response({

        'username': request.user.username,
        'message': 'Protected Route Accessed',

    })
    
@api_view(['POST'])
def login(request):

    try:

        print(request.data)

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        print("USER:", user)

        if user is None:
            if not User.objects.filter(username=username).exists():
                return Response({
                    "message": "User does not exist"
                }, status=404)
                
            if not User.objects.filter(password=password).exists():
                return Response({
                    "message": "Incorrect password"
                }, status=401)
                
            # return Response({
            #     "message": "Invalid credentials"
            # }, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login Successful',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })

    except Exception as e:

        print("LOGIN ERROR:", e)

        return Response({
            "error": str(e)
        }, status=500)
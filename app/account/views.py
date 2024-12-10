from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from rest_framework import serializers, generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from idea.models import Idea
from account.models import User


class RegistrationAPIView(APIView, mixins.CreateModelMixin):
    class UserCreateSerializer(serializers.Serializer):
        email = serializers.EmailField()
        username = serializers.CharField()
        password = serializers.CharField()

    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  # Создание Refesh и Access
            refresh.payload.update({    # Полезная информация в самом токене
                'user_id': user.id,
                'username': user.username
            })

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),  # Отправка на клиент
            }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView, mixins.CreateModelMixin):
    class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            return Response({'error': 'Нужен и логин, и пароль'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Неверные данные'},
                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })

        return Response(status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')  # С клиента нужно отправить refresh token
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавить его в чёрный список
        except Exception as e:
            return Response({'error': f'Неверный Refresh token {e}'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Выход успешен'},
                        status=status.HTTP_200_OK)


class Profile(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    class UserSerializer(serializers.Serializer):
        id = serializers.CharField()
        username = serializers.CharField()
        email = serializers.EmailField()
        about_me = serializers.CharField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        ideas = Idea.objects.filter(author__username=username)

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'username'
    

    # def get(self, request, *args, **kwargs):
    #     user = get_object_or_404(User, username=kwargs['username'])
    #     ideas = Idea.objects.filter(author__username=kwargs['username'])
    #     categories = Category.objects.all()

    #     user_data = UserSerializer(user).data
    #     ideas_data = IdeaSerializer(ideas, many=True).data
    #     categories_data = CategorySerializer(categories, many=True).data
        
    #     return Response({
    #         'user': user_data,
    #         'ideas': ideas_data,
    #         'categories': categories_data,
    #     })

    # def post(self, request):
    #     pass


@login_required(login_url='/login/')
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    ideas = Idea.objects.filter(author__username=username)
    if user.is_authenticated:
        if request.method == 'POST':
            profile_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Профиль изменен')
                return redirect(to='my_profile', username=username)
        else:
            profile_form = UpdateUserForm(instance=request.user)

        context = {
            'user': user,
            'profile_form': profile_form,
            'ideas': ideas,
            'title': 'Редактировать профиль',
        }
        return render(request, 'account/edit_profile.html', context=context)
    else:
        return redirect('login')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_message = "Пароль успешно изменен"
    success_url = reverse_lazy('index')

from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView


from rest_framework import (
    serializers,
    generics,
    viewsets,
    status,
    mixins,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)

from idea.models import Idea, Category
from account.models import User
from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            login(request, user)
            return Response({"message": "Успешный вход"}, status=status.HTTP_200_OK)
        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Успешный выход"}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView, mixins.UpdateModelMixin):
    class UserSerializer(serializers.Serializer):
        id = serializers.CharField()
        username = serializers.CharField()
        email = serializers.EmailField()
        about_me = serializers.CharField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        ideas = Idea.objects.filter(author__username=username)

    class IdeaSerializer(serializers.Serializer):
        id = serializers.CharField()
        title = serializers.CharField(max_length=100)
        description = serializers.CharField()
        time_create = serializers.DateTimeField()
        time_update = serializers.DateTimeField()
        author_id = serializers.IntegerField()
        category_id = serializers.IntegerField()

    class CategorySerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField(max_length=100)
        slug = serializers.SlugField(max_length=50)

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        ideas = Idea.objects.filter(author__username=kwargs['username'])
        categories = Category.objects.all()

        user_data = self.UserSerializer(user).data
        ideas_data = self.IdeaSerializer(ideas, many=True).data
        categories_data = self.CategorySerializer(categories, many=True).data

        return Response({
            'user': user_data,
            'ideas': ideas_data,
            'categories': categories_data,
        })

    def patch(self, request, *args, **kwargs):
        print(f"ДАТА - {request.data}")
        user = User.objects.get(username=kwargs['username'])
        print(user)
        user.email = request.data['email']
        user.about_me = request.data['about_me']
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']

        user.save()

        return Response({}, status=status.HTTP_201_CREATED)


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

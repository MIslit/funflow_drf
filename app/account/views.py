from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from rest_framework import serializers, generics, authentication, exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny


from idea.models import Idea
from account.models import User

from .serializers import (
    UserCreateSerializer,
    LoginSerializer,
)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)




# class LoginView(generics.CreateAPIView):
#     class LoginSerializer(serializers.Serializer):
#         username = serializers.CharField()
#         password = serializers.CharField()

#     permission_classes = (AllowAny, )
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         print(request.auth)
#         # serializer = self.serializer_class(data=request.data)
#         # serializer.is_valid(raise_exception=True)

#         # user = serializer.validated_data['username']

#         # update_last_login(None, user)
#         # data = get_user_profile_data(user)

#         return Response({}, status=status.HTTP_200_OK)


def logout_user(request):
    logout(request)
    return redirect('index')


class ProfileAPIVeiew(generics.RetrieveUpdateAPIView):
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

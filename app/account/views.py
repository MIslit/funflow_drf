# from django.contrib import messages
# from django.contrib.auth import logout, login
# from django.contrib.auth.decorators import login_required
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.views import PasswordChangeView
# from django.shortcuts import get_object_or_404, render, redirect
# from django.urls import reverse_lazy

# from rest_framework import serializers
# from rest_framework import generics
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny

# from django.contrib.auth.models import update_last_login
# from django.contrib.auth import authenticate

# from rest_framework.response import Response
# from rest_framework import status


# from account.models import User
# from .forms import UpdateUserForm
# from .serializers import (
#     CategorySerializer,
#     IdeaSerializer,
#     UserSerializer,
#     UserCreateSerializer,
#     LoginSerializer,
# )


# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer
#     permission_classes = (AllowAny, )


# class UserSessionLoginApi(APIView):
#     class InputSerializer(serializers.Serializer):
#         email = serializers.EmailField()
#         password = serializers.CharField()

#     def post(self, request):
#         serializer = self.InputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = authenticate(request, **serializer.validated_data)

#         if user is None:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         login(request, user)

#         data = user_get_login_data(user=user)
#         session_key = request.session.session_key

#         return Response({"session": session_key, "data": data})


# class LoginView(generics.CreateAPIView):
#     permission_classes = (AllowAny, )
#     serializer_class = LoginSerializer

#     def get(self, request, *args, **kwargs):
#         return Response({})

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user']

#         # Update last logged in
#         update_last_login(None, user)
#         data = get_user_profile_data(user)

#         return Response(data, status=status.HTTP_200_OK)


# def logout_user(request):
#     logout(request)
#     return redirect('index')


# class ProfileAPIVeiew(generics.RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)
#     lookup_field = 'username'
    


#     # def get(self, request, *args, **kwargs):
#     #     user = get_object_or_404(User, username=kwargs['username'])
#     #     ideas = Idea.objects.filter(author__username=kwargs['username'])
#     #     categories = Category.objects.all()

#     #     user_data = UserSerializer(user).data
#     #     ideas_data = IdeaSerializer(ideas, many=True).data
#     #     categories_data = CategorySerializer(categories, many=True).data
        
#     #     return Response({
#     #         'user': user_data,
#     #         'ideas': ideas_data,
#     #         'categories': categories_data,
#     #     })

#     # def post(self, request):
#     #     pass


# @login_required(login_url='/login/')
# def edit_profile(request, username):
#     user = get_object_or_404(User, username=username)
#     ideas = Idea.objects.filter(author__username=username)
#     if user.is_authenticated:
#         if request.method == 'POST':
#             profile_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
#             if profile_form.is_valid():
#                 profile_form.save()
#                 messages.success(request, 'Профиль изменен')
#                 return redirect(to='my_profile', username=username)
#         else:
#             profile_form = UpdateUserForm(instance=request.user)

#         context = {
#         'user': user,
#         'profile_form': profile_form,
#         'ideas': ideas,
#         'title': 'Редактировать профиль',
#     }
#         return render(request, 'account/edit_profile.html', context=context)
#     else:
#         return redirect('login')


# class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
#     template_name = 'account/change_password.html'
#     success_message = "Пароль успешно изменен"
#     success_url = reverse_lazy('index')

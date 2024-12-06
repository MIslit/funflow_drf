# from django.contrib.auth import authenticate

# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator

# from drf_registration.utils.users import (
#     has_user_verified,
# )

# from drf_registration.exceptions import (
#     NotActivated,
#     LoginFailed,
# )

# from idea.models import User, Category
# from 


# class IdeaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Idea
#         fields = ('id', 'title', 'description', 'time_create',
#                 'time_update', 'author_id', 'category_id', 'category')


# class UserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     ideas = Idea.objects.filter(author__username=username)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name',
#                   'about_me', 'avatar', 'ideas')


# class UserCreateSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     username = serializers.CharField(
#         validators=[UniqueValidator(queryset=User.objects.all())]
#         )
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         help_text='Leave empty if no change needed',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )

#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password')

#     def create(self, validated_data):
#         user = super(UserCreateSerializer, self).create(validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         return user


# class LoginSerializer(serializers.ModelSerializer):
#     """
#     User login serializer
#     """

#     username = serializers.CharField()
#     password = serializers.CharField()

#     class Meta:
#         model = User
#         fields = ('username', 'password')

#     def validate(self, data):
#         user = authenticate(**data)
#         if user:
#             # Check user is activated or not
#             if has_user_verified(user):
#                 # added user model to OrderedDict that serializer is validating
#                 data['user'] = user
#                 return data
#             raise NotActivated()
#         raise LoginFailed()


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('name', 'slug')


# class IndexSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()

#     class Meta:
#         model = Idea
#         fields = ('id', 'title', 'description', 'time_create',
#                 'time_update', 'author_id', 'category_id', 'category')


# class IdeaDetailSerializer(serializers.ModelSerializer):
#     categories = CategorySerializer(many=True, read_only=True)

#     class Meta:
#         model = Idea
#         fields = ('id', 'title', 'description', 'time_create',
#             'time_update', 'author_id', 'category_id', 'categories')

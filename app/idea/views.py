from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render


from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from .mail import send_email
from . import services
from . import selectors


class IndexAPIView(APIView):
    '''
    List of all ideas / Home page
    '''

    class CategorySerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField(max_length=30)
        slug = serializers.SlugField(max_length=10)

    class IndexSerializer(serializers.Serializer):
        id = serializers.CharField()
        title = serializers.CharField(max_length=100)
        description = serializers.CharField()
        time_create = serializers.DateTimeField()
        time_update = serializers.DateTimeField()
        author_id = serializers.IntegerField()
        category_id = serializers.IntegerField()

    permission_classes = (AllowAny,)

    def get(self, request):
        categories = selectors.get_all_categories()
        ideas = selectors.get_all_ideas()

        categories_data = self.CategorySerializer(categories, many=True).data
        ideas_data = self.IndexSerializer(ideas, many=True).data

        return Response({
            'categories': categories_data,
            'ideas': ideas_data,
        })

    def post(self, request):
        '''
        Search ideas in home page
        '''

        searched = request.data['searched']
        categories = selectors.get_all_categories()
        ideas = selectors.get_searched_ideas(searched)

        categories_data = self.CategorySerializer(categories, many=True).data
        ideas_data = self.IndexSerializer(ideas, many=True).data

        return Response({
            'categories': categories_data,
            'ideas': ideas_data,
        })


class IdeaCategoryAPIView(APIView):
    '''
    List of ideas by category
    '''

    class CategorySerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField(max_length=100)
        slug = serializers.SlugField(max_length=50)

    class IndexSerializer(serializers.Serializer):
        id = serializers.CharField()
        title = serializers.CharField(max_length=100)
        description = serializers.CharField()
        time_create = serializers.DateTimeField()
        time_update = serializers.DateTimeField()
        author_id = serializers.IntegerField()
        category_id = serializers.IntegerField()

    permission_classes = (AllowAny,)

    def get(self, request):
        categories = selectors.get_all_categories()
        ideas = selectors.get_idea_by_category(request.data['category_slug'])

        categories_data = self.CategorySerializer(categories, many=True).data
        ideas_data = self.IndexSerializer(ideas, many=True).data

        return Response({
            'categories': categories_data,
            'ideas': ideas_data,
        })


class IdeaDetailAPIView(APIView):
    '''
    One idea page
    '''

    class CategorySerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField(max_length=100)
        slug = serializers.SlugField(max_length=50)

    class IdeaDetailSerializer(serializers.Serializer):
        id = serializers.CharField()
        title = serializers.CharField(max_length=100)
        description = serializers.CharField()
        time_create = serializers.DateTimeField()
        time_update = serializers.DateTimeField()
        author = serializers.CharField()
        category = serializers.CharField()

    class CommentSerializer(serializers.Serializer):
        id = serializers.CharField()
        author = serializers.CharField()
        text = serializers.CharField(max_length=250)
        score = serializers.ChoiceField(selectors.SCORE_CHOICES)

    permission_classes = (AllowAny,)

    def get(self, request, **kwargs):
        idea = selectors.get_one_idea(kwargs['pk'])
        categories = selectors.get_all_categories()
        comments = selectors.get_comments_for_one_idea(kwargs['pk'])

        idea_data = self.IdeaDetailSerializer(idea, many=True).data
        categories_data = self.CategorySerializer(categories, many=True).data
        comments_data = self.CommentSerializer(comments, many=True).data

        return Response({
            'categories': categories_data,
            'idea': idea_data,
            'comments': comments_data,
        })

    def post(self, request, **kwargs):
        '''
        Add new comment for this idea
        '''

        pk = kwargs['pk']
        idea = selectors.get_one_idea(pk)
        categories = selectors.get_all_categories()
        comments = selectors.get_comments_for_one_idea(pk)

        idea_data = self.IdeaDetailSerializer(idea, many=True).data
        categories_data = self.CategorySerializer(categories, many=True).data
        comments_data = self.CommentSerializer(comments, many=True).data

        service = services.AddNewCommentService(request, pk)
        add_comment = service.create()

        messages.success(request, 'Комментарий добавлен')

        return Response({
            'categories': categories_data,
            'idea': idea_data,
            'comments': comments_data,
        })


class AddIdeaAPIView(APIView):
    class CategorySerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField(max_length=100)
        slug = serializers.SlugField(max_length=50)

    class IdeaDetailSerializer(serializers.Serializer):
        id = serializers.CharField()
        title = serializers.CharField(max_length=100)
        description = serializers.CharField()
        author_id = serializers.IntegerField()
        category_id = serializers.ChoiceField(selectors.CATEGORY)

    permission_classes = (AllowAny,)

    def get(self, request):
        categories = selectors.get_all_categories()

        categories_data = self.CategorySerializer(categories, many=True).data

        return Response({
            'categories': categories_data,
        })

    def post(self, request):
        service = services.AddNewIdeaService(request)
        add_idea = service.create()

        messages.success(request, 'Идея добавлена')
        send_email.delay()

        return HttpResponseRedirect(reverse('index'))


class CategoriesAPIView(APIView):
    '''
    Page of all categories
    '''

    class CategorySerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        slug = serializers.SlugField()

    permission_classes = (AllowAny,)

    def get(self, request):
        categories = selectors.get_all_categories()
        categories_data = self.CategorySerializer(categories, many=True).data

        return Response({
            'categories': categories_data,
        })


def about(request):
    categories = selectors.get_all_categories()
    context = {
        'title': 'О нас',
        'categories': categories,
    }

    return render(request, 'idea/about.html', context)

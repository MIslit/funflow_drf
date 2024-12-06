from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('', views.IndexAPIView.as_view(), name='index'),
    path('search/<str:searched>/', views.IndexAPIView.as_view(), name='search_results'),
    path('idea_detail/<int:pk>/', views.IdeaDetailAPIView.as_view(), name='idea'),
    path('category/<slug:category_slug>/', views.IdeaCategoryAPIView.as_view(), name='category'),
    path('categories/', views.CategoriesAPIView.as_view(), name='categories'),
    path('add_idea/', views.AddIdeaAPIView.as_view(), name='add_idea'),
    path('about/', views.about, name='about'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
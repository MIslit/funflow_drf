from django.db.models import Q

from .models import Idea, Category, Comment


SCORE_CHOICES = (
    ('УЖАСНО', '1'),
    ('ПЛОХО', '2'),
    ('НОРМАЛЬНО', '3'),
    ('ХОРОШО', '4'),
    ('ОТЛИЧНО', '5'),
)

CATEGORY = (
    ('1', 'Дома'),
    ('2', 'На улице'),
    ('3', 'Что-нибудь попробовать'),
)


def get_all_ideas():
    return Idea.objects.all()


def get_one_idea(pk):
    return Idea.objects.filter(pk=pk)


def get_searched_ideas(searched):
    return Idea.objects.filter(
            Q(title__contains=searched) | Q(description__contains=searched))


def get_idea_by_category(category):
    return Idea.objects.filter(category__slug=category)


def get_all_categories():
    return Category.objects.all()


def get_comments_for_one_idea(pk):
    return Comment.objects.select_related().filter(idea_id=pk)

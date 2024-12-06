from django.db import transaction

from .models import Idea, Comment


class AddNewIdeaService:
    def __init__(self, request):
        self.request = request

    @transaction.atomic
    def create(self):
        try:
            new_idea = Idea(
                title=self.request.data.get('title'),
                description=self.request.data.get('description'),
                author_id=self.request.user.id,
                category_id=self.request.data.get('category_id'),
            )
            new_idea.save()
            return new_idea

        except Exception as e:
            return f"Ошибка {e}"


class AddNewCommentService:
    def __init__(self, request, idea_id):
        self.request = request
        self.idea_id = idea_id

    @transaction.atomic
    def create(self):
        try:
            new_comment = Comment(
                text = self.request.data['text'],
                score = self.request.data['score'],
                author_id = self.request.data['author_id'],
                idea_id = self.idea_id,
            )
            new_comment.save()
            return new_comment

        except Exception as e:
            return f"Ошибка {e}"

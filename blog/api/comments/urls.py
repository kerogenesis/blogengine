from django.urls import path

from blog.api.comments.views import *

urlpatterns = [
    path('', CommentsListAPIView.as_view(), name='comments_list_api_url'),
    path('create/', CommentCreateAPIView.as_view(), name='comment_create_api_url'),
    path('<str:id>/', CommentDetailAPIView.as_view(), name='comment_detail_api_url')
]

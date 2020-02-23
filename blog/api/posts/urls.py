from django.urls import path

from blog.api.posts.views import *

urlpatterns = [
    path('', PostsListAPIView.as_view(), name='posts_list_api_url'),
    path('create', PostCreateAPIView.as_view(), name='post_create_api_url'),
    path('<str:slug>/', PostDetailAPIView.as_view(), name='post_detail_api_url'),
    path('<str:slug>/update/', PostUpdateAPIView.as_view(), name='post_update_api_url'),
    path('<str:slug>/delete/', PostDeleteAPIView.as_view(), name='post_delete_api_url'),
]

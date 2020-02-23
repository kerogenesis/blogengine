from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from blog.sitemaps import PostSitemap

from .feeds import LatestPostsFeed
from .views import *

sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path('', IndexPage.as_view(), name='index_page_url'),
    path('all/', posts_list, name='posts_list_url'),
    path('all/create/', PostCreate.as_view(), name='post_create_url'),
    path('all/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('all/<str:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('all/<str:slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
    path('all/<str:slug>/comments/create', CommentCreate.as_view(), name='comment_create_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tags/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tags/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tags/<str:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tags/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="blog/robots.txt", content_type='text/plain')),
    path('rss', LatestPostsFeed(), name='post_feed'),
    path('api/v1/posts/', include('blog.api.posts.urls'), name='blog-posts-api'),
    path('api/v1/comments/', include('blog.api.comments.urls'), name='blog-comments-api')
]

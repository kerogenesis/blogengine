from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from blog.models import Comment

from .serializers import (CommentCreateSerializer, CommentDetailSerializer,
                          CommentsListSerializer)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CommentCreateSerializer


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.all()
    lookup_field = 'id'
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentsListAPIView(ListAPIView):
    queryset = Comment.objects.filter(parent_id__exact=None)
    lookup_field = 'id'
    serializer_class = CommentsListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'body', 'created_on']
    permission_classes = [AllowAny]

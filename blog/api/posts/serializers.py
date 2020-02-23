from rest_framework.serializers import (HyperlinkedIdentityField,
                                        ModelSerializer, SerializerMethodField)

from blog.api.comments.serializers import CommentsListSerializer
from blog.models import Post


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'body',
            'tags',
            'og_image',
            'allow_comments'
        ]


class PostDetailSerializer(ModelSerializer):
    body = SerializerMethodField()
    comments = SerializerMethodField()
    comments_count = SerializerMethodField()
    reading_time = SerializerMethodField()
    url = HyperlinkedIdentityField(
        view_name='post_detail_api_url',
        lookup_field='slug'
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'reading_time',
            'title',
            'url',
            'body',
            'date_pub',
            'comments_count',
            'comments'
        ]

    @staticmethod
    def get_reading_time(obj):
        return str(obj.reading_time) + ' мин'

    @staticmethod
    def get_body(obj):
        return str(obj.formatted_markdown())

    def get_comments(self, obj):
        comments_qs = obj.get_comments_without_replies()
        comments = CommentsListSerializer(
            comments_qs,
            context=self.context,
            many=True
        ).data
        return comments

    @staticmethod
    def get_comments_count(obj):
        return str(obj.get_comments_without_replies().count())


class PostListSerializer(ModelSerializer):
    body = SerializerMethodField()
    url = HyperlinkedIdentityField(
        view_name='post_detail_api_url',
        lookup_field='slug'
    )
    comments_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'title',
            'url',
            'body',
            'date_pub',
            'comments_count'
        ]

    @staticmethod
    def get_body(obj):
        return str(obj.formatted_markdown())

    @staticmethod
    def get_comments_count(obj):
        return str(obj.get_comments_without_replies().count())

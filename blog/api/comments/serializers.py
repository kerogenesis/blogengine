from rest_framework.serializers import (
    HyperlinkedIdentityField, ModelSerializer, SerializerMethodField,
    ValidationError)

from blog.models import Comment, Post


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'name',
            'body'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request_object = self.context['request']
        parent_id = request_object.query_params.get('parent_id', None)
        self.slug = request_object.query_params.get('slug')
        self.parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id__exact=parent_id)
            if parent_qs.exists():
                self.parent_id = parent_id

    def validate(self, data):
        obj_qs = Post.objects.filter(slug=self.slug)
        if not obj_qs.exists() or obj_qs.count() != 1:
            raise ValidationError("Пост с таким УРЛом не найден")
        return data

    def create(self, validated_data):
        name = validated_data.get('name')
        body = validated_data.get('body')
        post_id = Post.objects.get(slug=self.slug).id
        comment = Comment(
            name=name,
            body=body,
            post_id=post_id,
            parent_id=self.parent_id
        )
        comment.save()
        return validated_data


class CommentChildSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='comment_detail_api_url',
        lookup_url_kwarg='id',
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'parent_id',
            'mark',
            'name',
            'body',
            'created_on',
            'url'
        ]


class CommentDetailSerializer(ModelSerializer):
    parent_post_url = SerializerMethodField()
    replies = SerializerMethodField()
    replies_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'mark',
            'name',
            'body',
            'created_on',
            'parent_post_url',
            'replies_count',
            'replies'
        ]
        read_only_fields = [
            'parent_post_url',
            'created_on',
            'replies_count',
            'replies'
        ]

    @staticmethod
    def get_parent_post_url(obj):
        try:
            return obj.get_api_url()
        except:
            return None

    @staticmethod
    def get_replies_count(obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(
                obj.children(),
                context=self.context,
                many=True
            ).data
        return None


class CommentsListSerializer(ModelSerializer):
    replies_count = SerializerMethodField()
    url = HyperlinkedIdentityField(
        view_name='comment_detail_api_url',
        lookup_url_kwarg='id',
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'name',
            'body',
            'created_on',
            'url',
            'replies_count'
        ]

    @staticmethod
    def get_replies_count(obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

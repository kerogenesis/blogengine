import datetime
import math
import re
from random import randint

import bleach
from bleach_whitelist import markdown_attrs, markdown_tags
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, blank=True, unique=True, verbose_name='УРЛ')
    body = MarkdownxField(blank=True, db_index=False, verbose_name='Текст')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts', verbose_name='Теги')
    reading_time = models.PositiveSmallIntegerField(default=0, verbose_name='Время чтения')
    og_image = models.URLField(default="https://res.cloudinary.com/wark/image/upload/v1582458310/og_default.jpg",
                               verbose_name='Картинка для соцсетей')
    allow_comments = models.BooleanField(default=True, verbose_name='Открытые комментарии')
    date_pub = models.DateTimeField(auto_now_add=True)

    def formatted_markdown(self):
        return markdownify(self.body)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def get_comments_without_replies(self):
        return Comment.objects.filter(post_id=self.id, parent_id=None)

    def get_replies(self):
        return Comment.objects.filter(post_id=self.id).exclude(parent_id=None)

    def get_reading_time(self):
        # convert markdown text to html code
        article_html = markdownify(self.body)

        # count words
        world_string = strip_tags(article_html)
        matching_words = re.findall(r'\w+', world_string)
        count = len(matching_words)

        # reading time
        # assuming 200wpm reading
        reading_time_min = math.ceil(count/200.0)
        return int(reading_time_min)

    def save(self, *args, **kwargs):
        if self.body:
            self.reading_time = self.get_reading_time()

        if not self.slug:
            new_slug = slugify(self.title, allow_unicode=True)
            self.slug = new_slug + '-' + str(int(datetime.datetime.now().microsecond))
        super().save(*args, **kwargs)

    @staticmethod
    def current_year():
        return str(datetime.datetime.now().year)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='УРЛ')

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Родитель')
    name = models.CharField(max_length=30, verbose_name='Имя')
    body = MarkdownxField(max_length=3000, blank=False, db_index=False, verbose_name='Текст')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    mark = models.BooleanField(default=False, verbose_name='Маркер')

    def children(self):  # replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        return self.parent is None

    @staticmethod
    def current_year():
        return str(datetime.datetime.now().year)

    def formatted_markdown(self):
        return bleach.clean(markdownify(self.body), markdown_tags, markdown_attrs)

    @staticmethod
    def gen_avatar():
        user_avatar_id = randint(1, 16)
        return "{}.jpg".format(user_avatar_id)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.post.slug}) + "#comment{}".format(self.id)

    def get_delete_url(self):
        return reverse('comment_delete_url', kwargs={'slug': self.post.slug, 'id': self.id})

    def get_api_url(self):
        return 'https://warkentin.ru' + reverse('post_detail_api_url', kwargs={'slug': self.post.slug})

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return '{} пишет: «{}»'.format(self.name, self.body)

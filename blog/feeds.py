from django.contrib.syndication.views import Feed
from markdownx.utils import markdownify

from .models import Post


class LatestPostsFeed(Feed):
    title = "Define yourself outside vim"
    link = "https://warkentin.ru/blog/"
    description = 'Из недавнего'
    author_name = 'Дмитрий Варкентин'
    language = 'ru'

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdownify(item.body)

    def item_content(self, item):
        return markdownify(item.content)

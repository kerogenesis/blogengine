from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.views.generic import View

from .forms import CommentForm, PostForm, TagForm
from .mixins import *


class IndexPage(View):
    template = 'blog/index.html'

    def get(self, request):
        posts = self.search_monitor(request)

        if not posts:
            return render(request, 'blog/post_not_found.html')

        pagintator = self.paginator(request, posts)
        return render(request, self.template, context=pagintator)

    @staticmethod
    def search_monitor(request):
        search_query = request.GET.get('search', '')
        if search_query:
            posts = Post.objects.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=search_query)
        else:
            posts = Post.objects.all()
        return posts

    @staticmethod
    def paginator(request, posts):
        posts_on_the_page = 6
        paginator = Paginator(posts, posts_on_the_page)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_page_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_page_url = ''
        if page.has_next():
            next_page_url = '?page={}'.format(page.next_page_number())
        else:
            next_page_url = ''

        pagintator_context = {
            'page_object': page,
            'is_paginated': is_paginated,
            'next_page_url': next_page_url,
            'prev_page_url': prev_page_url
        }
        return pagintator_context


class PostDetail(View):
    template_name = 'blog/post_detail.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug__iexact=slug)
        comments = post.comments.filter(parent=None)
        comment_form = CommentForm()
        context = {Post.__name__.lower(): post,
                   'admin_object': post,
                   'comments': comments,
                   'comment_form': comment_form}
        return render(request, self.template_name, context=context)


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    redirect_url = 'index_page_url'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'index_page_url'
    raise_exception = True


def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts_list.html', context={'posts': posts})


class CommentCreate(View):
    def post(self, request, slug):
        current_post = get_object_or_404(Post, slug__iexact=slug)
        bound_comments_form = CommentForm(data=request.POST)
        if bound_comments_form.is_valid():
            new_comment = bound_comments_form.save(commit=False)

            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None
            if parent_id is not None:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    new_comment.parent = parent_qs.first()
                    new_comment.post = current_post
                    new_comment.save()
                    return redirect(
                        reverse('post_detail_url',
                                kwargs={'slug': slug}) + '#comment{}'.format(parent_id)
                    )

            new_comment.post = current_post
            new_comment.save()
            return redirect(new_comment)
        return redirect('/')


class CommentMark(LoginRequiredMixin, View):
    def get(self, request, slug, id):
        comment_for_mark = Comment.objects.get(id=id)
        if not comment_for_mark.mark:
            comment_for_mark.mark = True
        else:
            comment_for_mark.mark = False
        comment_for_mark.save()
        if comment_for_mark.parent_id is not None:
            return redirect(
                reverse('post_detail_url', kwargs={'slug': slug}) + '#comment{}'.format(comment_for_mark.parent_id)
            )
        else:
            return redirect(comment_for_mark)


class CommentDelete(LoginRequiredMixin, View):
    model = Comment

    def get(self, request, slug, id):
        comment_for_delete = self.model.objects.get(id=id)
        context = {self.model.__name__.lower(): comment_for_delete}
        return render(request, 'blog/comment_delete_form.html', context=context)

    def post(self, request, slug, id):
        comment_for_delete = self.model.objects.get(id=id)
        comment_for_delete.delete()
        return redirect(reverse('post_detail_url', kwargs={'slug': slug}) + '#comments')


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})

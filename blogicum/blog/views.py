from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.views.generic.edit import ModelFormMixin

import blogicum.constans as const
from .forms import CommentForm, PostForm
from .mixins import ChangingCommentMixin, OnlyAuthorMixin
from .models import Category, Comment, Post, User


class CategoryPostsListView(ListView):
    model = Category
    paginate_by = const.COUNT_POSTS_ON_PAGE
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get_object(self):
        return get_object_or_404(
            Category.objects.filter(
                slug=self.kwargs.get('category_slug', None),
                is_published=True
            )
        )

    def get_queryset(self):
        return self.get_object().posts(manager='published_posts').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        post = super().get_object()
        if post.author != self.request.user:
            return get_object_or_404(
                Post.published_posts,
                pk=self.kwargs.get('post_id', None)
            )
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.get_object().comments.select_related('author')
        )
        return context


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(OnlyAuthorMixin, ModelFormMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:index')


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = const.COUNT_POSTS_ON_PAGE
    queryset = Post.published_posts.all().annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date', 'title')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_model = None
    model = Comment
    pk_url_kwarg = 'comment_id'
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_model = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_model
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.post_model.pk}
        )


class CommentUpdateView(OnlyAuthorMixin, ChangingCommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(OnlyAuthorMixin, ChangingCommentMixin, DeleteView):
    pass


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ('username', 'first_name', 'last_name', 'email',)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.username}
        )


class ProfileDetailView(ListView):
    model = User
    paginate_by = const.COUNT_POSTS_ON_PAGE
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_object(self):
        return get_object_or_404(
            User.objects.filter(username=self.kwargs.get('username', None))
        )

    def get_queryset(self):
        user = self.get_object()
        if self.get_object() == self.request.user:
            return user.posts(manager='objects').all().annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date', 'title')
        return user.posts(manager='published_posts').all().annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

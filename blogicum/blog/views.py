from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import MultipleObjectMixin

import blogicum.constans as const

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post, User


class CategoryPostsDetailView(MultipleObjectMixin, DetailView):
    model = Category
    paginate_by = const.COUNT_POSTS_ON_PAGE
    template_name = 'blog/category.html'

    def get_object(self):
        return get_object_or_404(
            Category.objects.filter(
                slug=self.kwargs.get('slug', None),
                is_published=True
            )
        )

    def get_context_data(self, **kwargs):
        object_list = self.object.posts(manager='published_posts').all()
        context = super(CategoryPostsDetailView, self).get_context_data(
            object_list=object_list, **kwargs
        )
        context['category'] = self.object
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            get_object_or_404(Post.published_posts, pk=kwargs.get('pk', None))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', pk=self.get_object().pk)


class PostDeleteView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     ModelFormMixin,
                     DeleteView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        object = self.get_object()
        return redirect('blog:post_detail', pk=object.pk)


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = const.COUNT_POSTS_ON_PAGE
    queryset = Post.published_posts.all()


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
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_model = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_model
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_model.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post_id})

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', pk=self.get_object().post_id)


class CommentDeleteView(LoginRequiredMixin,
                        UserPassesTestMixin,
                        DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post_id})

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', pk=self.get_object().post_id)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = UserForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'slug': self.object.username})


class ProfileDetailView(DetailView, MultipleObjectMixin):
    model = User
    paginate_by = const.COUNT_POSTS_ON_PAGE
    template_name = 'blog/profile.html'
    slug_field = 'username'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        if self.request.user == self.object:
            object_list = self.object.posts(manager='objects').all()
        else:
            object_list = self.object.posts(manager='published_posts').all()
        context = super(ProfileDetailView, self).get_context_data(
            object_list=object_list, **kwargs
        )
        return context

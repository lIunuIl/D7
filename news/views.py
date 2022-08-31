from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from django.shortcuts import render, reverse, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .forms import PostForm, ProfileUserForm
from .models import Post, User
from .filters import PostFilter

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        #context['posts'] = 3
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')


class PostSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class ProfileUserUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    model = User
    template_name = 'user_edit.html'
    success_url = reverse_lazy('news')

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class MyView(PermissionRequiredMixin, View):
    permission_required = ('news.Can_add_post',
                           'news.Can_change_post',
                           'news.Can_delete_post')


class PostView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news.html', {})

    def send(self, request, *args, **kwargs):
        post = Post(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            user_name=request.POST['user_name'],
            message=request.POST['message'],
        )
        post.save()

        html_content = render_to_string(
            'post_created.html',
            {
                'post': post,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{post.user_name}{post.date.strftime("%Y-%M-%d")}',   # имя клиента и дата записи будут в теме для удобства
            body=post.message,   # сообщение с кратким описанием проблемы
            from_email='goldenteacherr@yandex.ru',      # здесь указываете почту, с которой будете отправлять
            to=['g.teacher@bk.ru'],       # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()

        return redirect('posts:subscribe')
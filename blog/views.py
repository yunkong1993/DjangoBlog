from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponse
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from .models import Category, Post, Tag
from visits.views import change_info


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    paginate_by = 10


class AboutView(TemplateView):
    model = Post
    template_name = "blog/about.html"
    context_object_name = "about"


class ContactView(TemplateView):
    model = Post
    template_name = "blog/contact.html"
    context_object_name = "contact"


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get("pk"))
        q = super().get_queryset().filter(category=cate)
        if self.request.user.is_authenticated:  # 如果有用户登陆
            return q.filter(Q(is_private=False) | Q(author=self.request.user))
        else:
            return q.filter(is_private=False)


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        q = super().get_queryset().filter(created_time__year=year, created_time__month=month)
        if self.request.user.is_authenticated:  # 如果有用户登陆
            return q.filter(Q(is_private=False) | Q(author=self.request.user))
        else:
            return q.filter(is_private=False)


class PrivateView(IndexView):
    def get_queryset(self):
        change_info(self.request)
        if self.request.user.is_authenticated:  # 如果有用户登陆
            return super().get_queryset().filter(Q(is_private=False) | Q(author=self.request.user))
        else:
            return super().get_queryset().filter(is_private=False)


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        q = super().get_queryset().filter(tags=t)
        if self.request.user.is_authenticated:  # 如果有用户登陆
            return q.filter(Q(is_private=False) | Q(author=self.request.user))
        else:
            return q.filter(is_private=False)


# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super().get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q), is_private=False)
    return render(request, 'blog/index.html', {'post_list': post_list})


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == 'admin' and password == '123456':
            return HttpResponse('login success')
        elif username == '' or password == '':
            return render(request, 'index.html', {'error1': 'username or password is null!'})
        else:
            return render(request, 'index.html', {'error2': 'username or password error!'})

from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .get_index import get_index_list
from .get_detail import get_detail
from .models import VideoDetailItem
from .AES import AesCrypto
from urllib.parse import quote
from django.conf import settings


class VideoView(TemplateView):
    # model = Post
    template_name = "video/video_index.html"
    context_object_name = "video"


class VideoDetailView(TemplateView):
    model = VideoDetailItem
    template_name = "video/video_detail.html"
    context_object_name = "video_detail"


def my_login_required(func):
    '''自定义 登录验证 装饰器'''

    def check_login_status(request):
        '''检查登录状态'''
        if request.user.is_authenticated:
            # 当前有用户登录，正常跳转
            return func(request)
        else:
            # 当前没有用户登录，跳转到登录页面
            error_msg = "需要登陆权限，请先登陆"
            messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
            return HttpResponseRedirect('/video')

    return check_login_status


@my_login_required
def search(request):
    q = request.GET.get('q')
    i = request.GET.get('carlist')
    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')
    q = quote(q)
    video_list = get_index_list(i=i, q=q)

    return render(request, 'video/video_index.html', {'video_list': video_list, 'i':i})


@my_login_required
def detail(request):
    m = request.GET.get('m')
    i = request.GET.get('carlist')
    if not m:
        error_msg = "无效地址"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    video_detail, video_items = get_detail(i=i, m=m)
    return render(request, 'video/video_detail.html', {'video_detail': video_detail, 'video_items': video_items})


@my_login_required
def play(request):
    p = request.GET.get('p')
    n = request.GET.get('n')

    if not p or not n:
        error_msg = "无效地址"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')
    my_crypt = AesCrypto(bytes(settings.AES_KEY, encoding='utf-8'))
    http = my_crypt.decrypt(p)
    name = my_crypt.decrypt(n)
    video_type = http[-4:]
    if 'm3u8' in video_type:
        play_type = "application/x-mpegURL"
    else:
        play_type = "video/mp4"
    return render(request, 'video/video_play.html', {'http': http, 'name': name, 'play_type': play_type})

from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.filter(is_private=False).order_by('-created_time')[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.filter(is_private=False).dates('created_time', 'month', order='DESC'),
    }


# @register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
# def show_tags(context):
#     return {
#         'tag_list': Tag.objects.all(),
#     }


# @register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
# def show_categories(context):
#     return {
#         'category_list': Category.objects.all(),
#     }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.filter(post__is_private=False).annotate(num_posts=Count('post')).filter(
        num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.filter(post__is_private=False).annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }

from django.urls import path
from . import views
from django.conf.urls import url, include
import os
from django.conf.urls.static import static
from django.conf import settings


app_name = 'blog'
urlpatterns = [
    path('', views.PrivateView.as_view(), name='index'),
    path('about', views.AboutView.as_view(), name='about'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('search/', views.search, name='search'),
    url(r'mdeditor/', include('mdeditor.urls')),

]
 
urlpatterns += static(r'media/editor/', document_root='C:/inetpub/wwwroot/django/uploads/editor')
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

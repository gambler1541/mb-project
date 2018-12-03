"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from config.settings import base
from posts.views import tag_post_list

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='posts:post_list'), name='index'),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('members/', include('members.urls')),
    path('explore/tags/<str:tag_name>/',tag_post_list,name='tag_post_list'),

]

urlpatterns += static(
    prefix=base.MEDIA_URL,
    document_root=base.MEDIA_ROOT,
)

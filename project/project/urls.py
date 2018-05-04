"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from project.PreDisulfideBond import views

urlpatterns = [
    # url(r'^PreDisulfideBond/', include('PreDisulfideBond.urls')),
    url(r'^index$', views.index, name='index'),
    url(r'^predict$', views.simple_upload, name='predict'),
	# url(r'^$', views.simple_upload, name='simple_upload'),
    url(r'^comments_upload/$', views.comments_upload, name='comments_upload'),
    url(r'^integration/$', views.integration, name='integration'),
    # url(r'^loadpdb/$', views.loadpdb, name='loadpdb'),
    url(r'^result$', views.result, name='result'),
    # url(r'^result$', views.simple_upload, name='result'),
    # url(r'^test/$', views.comments_upload, name='comments_upload'),
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
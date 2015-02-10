from django.conf.urls import patterns, include, url
from django.contrib import admin
import urls
from apps.blog import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gigsblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^gigs/login', views.Login.as_view(), name='login'),
    url(r'^gigs/signup', views.SignUp.as_view(), name='signup'),
    url(r'^gigs/logout', 'django.contrib.auth.views.logout',{'next_page':'/'}, name='logout'),
    url(r'^post/', include('urls.blog', namespace='post')),
)

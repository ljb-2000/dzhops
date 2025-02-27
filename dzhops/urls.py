from django.conf.urls import patterns, include, url
#from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dzhops.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'dzhops.views.index', name='index'),
    url(r'^login/$', 'dzhops.views.login',name='login'),
    #url(r'^accounts/logout/$', logout,{'template_name':'login.html'}, name='logout'),
    #url(r'^accounts/profile/$', 'dzhops.views.index', name='profile'),
    #url(r'^login/$', 'dzhops.views.login', name='login'),
    url(r'^common/', include('common.urls')),
    url(r'^hostlist/', include('hostlist.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

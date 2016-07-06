from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from opal.urls import urlpatterns as opatterns

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'stories/$', TemplateView.as_view(template_name='stories.html')),
)

urlpatterns += opatterns

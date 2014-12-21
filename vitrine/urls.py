from django.conf.urls import patterns, include, url

urlpatterns = patterns('vitrine.views',
    url(r'^json/(?P<json>\w+)/(?P<tri>\w+)', 'json'),
    url(r'^$', 'accueil'),
)

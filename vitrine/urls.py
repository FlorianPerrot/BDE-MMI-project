from django.conf.urls import patterns, include, url

urlpatterns = patterns('vitrine.views',
    url(r'^json/(?P<json>\w+)/(?P<tri>[\w|\W]+)', 'json'),
    url(r'^gallerie/(?P<nom_gallerie>[\w|\W]+)', 'gallerie', name="gallerie"),
    url(r'^$', 'accueil', name="accueil"),
)

from django.conf.urls import patterns, include, url

urlpatterns = patterns('vitrine.views',
    url(r'^json/(?P<json>\w+)/(?P<tri>[\w|\W]+)', 'json'),
    url(r'^galerie/(?P<nom_galerie>[\w|\W]+)', 'galerie', name="galerie"),
    url(r'^$', 'accueil', name="accueil"),
)

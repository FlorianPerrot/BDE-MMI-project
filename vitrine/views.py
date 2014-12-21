import datetime
from django.shortcuts import render
from vitrine.models import Actu, Event, Contact, Membre, Gallerie
from django.http import HttpResponse, Http404
from django.utils import timezone, simplejson
from django.shortcuts import render
from django.views.decorators.cache import never_cache

class JsonResponse(HttpResponse):
    def __init__(self, content, mimetype='application/json', status=None, content_type=None):super(JsonResponse, self).__init__(content=simplejson.dumps(content),mimetype=mimetype,status=status,content_type=content_type,)

@never_cache
def json(request, json, tri):
    if json == "actu" and tri == "all":
        return JsonResponse(
            news_to_dico(Actu.objects.all().order_by('-date')))
    elif json == "event" and tri == "historique":
        return JsonResponse(
            news_to_dico( Event.objects.filter(date__lt = timezone.now()).order_by('-date') ))
    elif json == "event" and tri == "prochainement":
        return JsonResponse(
            news_to_dico(Event.objects.filter(date__gte = timezone.now()).order_by('date') ))
    elif json =="event" and tri == "all":
        return JsonResponse(
           news_to_dico(Event.objects.all().order_by('-date') ))
    elif json == "contact" and tri == "all":
        return JsonResponse(contact_to_dico(Contact.objects.all()[:1]))
    elif json == "news":
        return JsonResponse([{"event":Event.objects.filter(date_ajout__gte = datetime.datetime.fromtimestamp(float(tri)/1000)).count(),
                             "actu":Actu.objects.filter(date__gte = datetime.datetime.fromtimestamp(float(tri)/1000)).count()}])
    elif json == "gallerie":
        if tri == "all":
            return JsonResponse(galerie_to_dico(Gallerie.objects.all().order_by('nom')))
        else:
            if len(Gallerie.objects.filter(nom = tri)) > 0:
                return JsonResponse(images_to_dico(Gallerie.objects.filter(nom = tri)[0].images.all()))
            else:
                return JsonResponse([])
            
            
            
    return JsonResponse([])

def accueil(request):
    events = list(Event.objects.all().filter(date__gte= timezone.now()).order_by('date')) + list(Event.objects.all().filter(date__lt = timezone.now()).order_by('-date'))
    galleries = []
    for gallerie in Gallerie.objects.all():
        galleries += [{"nom_gallerie":gallerie.nom,"titre_image":gallerie.images.all()[0].titre,"url_image":gallerie.images.all()[0].image.url}]
    return render(request, "base.html", {"actus":Actu.objects.all().order_by('-date')[:2],
                                            "events":events[:2],
                                            "galleries":galleries,
                                            "membres":Membre.objects.all().order_by('rang','nom'),
                                            "contact":Contact.objects.all()[0]})


def news_to_dico(models):
    dicoArray = []
    for model in models:
        dico = {"titre":model.titre,"contenu":model.contenu,"date":timezone.localtime(model.date).strftime("%d/%m/%Y %H:%M")}
        if type(model) is Event:
                        if bool(model.lieu):
                                dico.update({"lieu":model.lieu})
                        else:
                                dico.update({"lieu":""})
        if bool(model.image):
                        dico.update({"image":model.image.image.url})
        else:
                        dico.update({"image":""})
        dicoArray += [dico]
        
    return dicoArray

def contact_to_dico(models):
    return {"email":models[0].email,"adresse":models[0].adresse,"lien_facebook":models[0].lien_facebook,"lien_instagram":models[0].lien_instagram}

def galerie_to_dico(galleries):
    gallerieArray = []
    for  gallerie in galleries:
        dico = {}
        images = []
        for image in gallerie.images.all():
            imageTitre = image.titre
            if imageTitre is None:
                imageTitre = ""
            images += [{"titre":imageTitre,"url":image.image.url}]       
        dico.update({"nom":gallerie.nom})
        dico.update({"images":images})
        gallerieArray += [dico]
    return gallerieArray
        
def images_to_dico(images):
    imageArray = []
    for image in images:
        imageTitre = image.titre
        if imageTitre is None:
            imageTitre = ""
        imageArray += [{"titre":imageTitre,"url":image.image.url}]
    return imageArray

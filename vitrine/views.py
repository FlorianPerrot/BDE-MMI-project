import datetime
from django.shortcuts import render
from vitrine.models import Actu, Event, Contact, Membre, Galerie
from django.http import HttpResponse, HttpResponseNotFound, Http404
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
    elif json == "galerie":
        if tri == "all":
            return JsonResponse(galerie_to_dico(Galerie.objects.all().order_by('nom')))
        else:
            if len(Galerie.objects.filter(nom = tri)) > 0:
                return JsonResponse(images_to_dico(Galerie.objects.filter(nom = tri)[0].images.all()))
            else:
                return JsonResponse([])



    return JsonResponse([])

def accueil(request):
    events = list(Event.objects.all().filter(date__gte= timezone.now()).order_by('date')) + list(Event.objects.all().filter(date__lt = timezone.now()).order_by('-date'))
    galeries = []
    for galerie in Galerie.objects.all():
        galeries += [{"nom_galerie":galerie.nom,"titre_image":galerie.images.all()[0].titre,"url_image":galerie.images.all()[0].image.url}]
    return render(request, "base.html", {"actus":Actu.objects.all().order_by('-date')[:2],
                                            "events":events[:2],
                                            "galeries":galeries,
                                            "membres":Membre.objects.all().order_by('rang','nom'),
                                            "contact":Contact.objects.all()[:1]})


def galerie(request, nom_galerie):
    galerie = Galerie.objects.filter(nom = nom_galerie)
    print(len(galerie))
    if(len(galerie)>0):
        return render(request, "galerie_mobile.html", {"galerie":galerie[0]})
    else:
        raise Http404

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

def galerie_to_dico(galeries):
    galerieArray = []
    for  galerie in galeries:
        dico = {}
        images = []
        for image in galerie.images.all():
            imageTitre = image.titre
            if imageTitre is None:
                imageTitre = ""
            images += [{"titre":imageTitre,"url":image.image.url}]
        dico.update({"nom":galerie.nom})
        dico.update({"images":images})
        galerieArray += [dico]
    return galerieArray

def images_to_dico(images):
    imageArray = []
    for image in images:
        imageTitre = image.titre
        if imageTitre is None:
            imageTitre = ""
        imageArray += [{"titre":imageTitre,"url":image.image.url}]
    return imageArray

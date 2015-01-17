from django.db import models
from django.utils import timezone
from datetime import datetime


class Image(models.Model):
    titre = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='galerie')

    def apercu(self):
        return u'<img style="width:100px" src="{0}" />'.format(self.image.url)
    apercu.allow_tags = True

    def __unicode__(self):
        if self.titre == None :
            return u'Image {0}'.format(str(self.id))
        return self.titre

class Actu (models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ForeignKey(Image, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def apercu(self):
        if bool(self.image):
            return u'<img style="width:100px" src="{0}" />'.format(self.image.image.url)
        return u''
    apercu.allow_tags = True

    def __unicode__(self):
        return u'{0} - {1}'.format(self.titre,timezone.localtime(self.date).strftime("%d/%m/%Y %H:%M"))

class Event(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date = models.DateTimeField()
    image = models.ForeignKey(Image, null=True)
    lieu = models.CharField(max_length=200, null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def apercu(self):
        if bool(self.image):
            return u'<img style="width:100px" src="{0}" />'.format(self.image.image.url)
        return u''
    apercu.allow_tags = True

    def __unicode__(self):
        acroche = ""
        if self.date < timezone.now():
            acroche = "eu "
        return u'{0} - A {1}lieu le {2} - publié le {3}'.format(self.titre, acroche, timezone.localtime(self.date).strftime("%d/%m/%Y %H:%M"), timezone.localtime(self.date_ajout).strftime("%d/%m/%Y %H:%M"))

class Contact(models.Model):
    email = models.EmailField()
    adresse = models.CharField(max_length=200)
    lien_facebook = models.URLField()
    lien_instagram = models.URLField()

    def __unicode__(self):
        return self.email+" - "+self.adresse

class Galerie(models.Model):
    nom = models.CharField(max_length=200,primary_key=True)
    images = models.ManyToManyField(Image)

    def apercu(self):
        apercu = u''
        for image in self.images.all():
            apercu += image.apercu()
        return apercu
    apercu.allow_tags = True

    def __unicode__(self):
        return self.nom

class Membre(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='membres',default="membres/default.svg")
    status = models.CharField(max_length=50, null=True, blank=True)
    rang = models.IntegerField()

    def apercu(self):
        return u'<img style="width:100px" src="{0}" />'.format(self.photo.url)
    apercu.allow_tags = True

    def __unicode__(self):
        return self.prenom + " " + self.nom

from django.contrib import admin
from vitrine.models import Actu, Event, Contact, Image, Galerie, Membre

class ContactAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

class ImageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'apercu',)

class GalerieAdmin(admin.ModelAdmin):
    list_display = ('nom','apercu',)

class ActuAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date', 'apercu',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date', 'apercu',)

class MembreAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'status','rang','apercu',)

admin.site.register(Actu, ActuAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Galerie, GalerieAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Membre, MembreAdmin)

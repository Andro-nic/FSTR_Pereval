from django.contrib import admin
from .models import User, Coords, Pereval, Image

class UserAdmin(admin.ModelAdmin):
    list_display = ['id']


class CoordsAdmin(admin.ModelAdmin):
    list_display = ['id']


class PerevalAdmin(admin.ModelAdmin):
    list_display = ['id']


class ImageAdmin(admin.ModelAdmin):
    list_display = ['id']


admin.site.register(User, UserAdmin)
admin.site.register(Coords, CoordsAdmin)
admin.site.register(Pereval, PerevalAdmin)
admin.site.register(Image, ImageAdmin)

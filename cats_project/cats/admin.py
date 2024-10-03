from django.contrib import admin

from .models import Breed, Cat


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    pass

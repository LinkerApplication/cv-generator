from django.contrib import admin

from .models import Profile


class PlaceOfWorkInline(admin.StackedInline):
    model = Profile.places_of_work.through


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        PlaceOfWorkInline
    ]

from django.contrib import admin

from .forms import CustomUserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

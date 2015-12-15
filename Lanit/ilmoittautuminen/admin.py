# -*- coding: utf-8 -*-
# Ääkköset toimimaan

from django.contrib import admin
from .models import Lanittaja
from .models import Istumapaikka


# Muokataan adminnäkymää
class IstumaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "varattu", "maksettu", "omistaja"]
    class Meta:
        model = Istumapaikka


admin.site.register(Lanittaja)
admin.site.register(Istumapaikka, IstumaAdmin)
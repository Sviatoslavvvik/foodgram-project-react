from django.contrib import admin

from .models import Ingridient, Tag


class IngridientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)
    search_fields = ["name", "measurement_unit"]


admin.site.register(Ingridient, IngridientAdmin)
admin.site.register(Tag)

from django.contrib import admin

from .models import Favorite, ShoppingChart


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'receipe')


class ShoppingChartAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredients')

    def ingredients(self, obj):
        return obj.receipe.ingredients.all()


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingChart, ShoppingChartAdmin)

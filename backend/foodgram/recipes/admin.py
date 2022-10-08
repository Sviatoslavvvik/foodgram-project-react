from django.contrib import admin

from .models import IngredientInRecipe, Ingridient, Receipe, Tag


class IngridientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)
    search_fields = ["name", "measurement_unit"]


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'is_favorited',
    )
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def is_favorited(self, obj):
        return obj.favorite_receip.count()


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('receipe', 'ingridient', 'amount')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


admin.site.register(Ingridient, IngridientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Receipe, RecipeAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)

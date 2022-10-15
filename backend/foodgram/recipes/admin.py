from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Receipe, Tag


class IngridientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name', 'measurement_unit')


class RecipeIngredientInLine(admin.TabularInline):
    model = IngredientInRecipe


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
    inlines = [RecipeIngredientInLine]

    def is_favorited(self, obj):
        return obj.favorite_receip.count()


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('receipe', 'ingredient', 'amount')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


admin.site.register(Ingredient, IngridientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Receipe, RecipeAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    summernote_fields = ('preparation_steps')


admin.site.register(Category, CategoryAdmin)

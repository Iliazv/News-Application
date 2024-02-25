from django.contrib import admin
from .models import New, Tag


class TagInline(admin.StackedInline):
    model = Tag
    extra = 2

class NewAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    search_fields = ['title']
    list_display = ['title']

admin.site.register(New, NewAdmin)
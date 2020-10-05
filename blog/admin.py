from django.contrib import admin

from .models import ArticlePost, Tag, Category


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ArticlePost)

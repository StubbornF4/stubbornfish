from django.db.models import Q, F
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Tag, ArticlePost, Category
from config.models import SideBar

class PostDetailView(DetailView):
    model = ArticlePost
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'articlepost_id'

    def get(self, *args, **kwargs):
        response = super().get(self, *args, **kwargs)
        ArticlePost.objects.filter(pk=self.object.id).update(pv=F('pv')+1, uv=F('uv')+1)

        return response

class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.objects.all()
        })
        # 'navs', 'categories'
        context.update(Category.get_navs())
        return context

class IndexView(CommonViewMixin, ListView):
    queryset = ArticlePost.latest_posts()
    template_name = 'blog/list.html'
    context_object_name = 'article_list'
    paginate_by = 5

class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        #要用两个下划线！用来表示tag字段的id
        return queryset.filter(tag__id=tag_id)

class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(
            Q(title__icontains=keyword)
            | Q(desc__icontains=keyword)
        )




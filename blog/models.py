import mistune

from django.core.cache import cache
from django.db import models


#文章分类
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='名称')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    @classmethod
    def get_navs(cls):
        catogories = Category.objects.all()
        normal_cato = []
        nav_cato = []
        for item in catogories:
            if item.is_nav:
                nav_cato.append(item)
            else:
                normal_cato.append(item)

        return {
            'navs': nav_cato,
            'categories': normal_cato
        }

#文章标签
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'

#文章
class ArticlePost(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    body = models.TextField(verbose_name='正文', help_text="正文为Markdown格式")
    content_html = models.TextField(verbose_name='正文markdown代码', blank=True, editable=False)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        verbose_name='分类'
    )
    tag = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name='标签'
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-created_time']

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.articlepost_set.all()

        return post_list, category

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.articlepost_set.all()

        return post_list, tag

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.all()
        return queryset

    @classmethod
    def host_posts(cls):
        result = cache.get('host_posts')
        if not result:
            result = cls.objects.all().order_by('-pv')
            cache.set('host_posts', result, 60*10)
        return result

    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.body)
        super().save(self, *args, **kwargs)





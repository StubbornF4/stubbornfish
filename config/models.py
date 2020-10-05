from django.db import models
from django.template.loader import render_to_string


class SideBar(models.Model):
    SIDE_TYPE = (
        (1, 'HTML'),
        (2, '最新文章'),
        (3, '最热文章'),
    )
    title = models.CharField(max_length=50, verbose_name='标题')
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name='展示类型')
    contents = models.CharField(max_length=500, blank=True, help_text="如果不是html类型，可为空", verbose_name='内容')

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'

    def content_html(self):
        from blog.models import ArticlePost
        result = ''
        if self.display_type == 1:
            result = self.contents
        elif self.display_type == 2:
            context = {
                'posts': ArticlePost.latest_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == 3:
            context = {
                'posts': ArticlePost.host_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        return result

    def __str__(self):
        return self.title


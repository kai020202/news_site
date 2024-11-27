from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Post(models.Model):
    title = models.CharField(max_length=200) 
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class News(models.Model):
    title = models.CharField(max_length=255)  # ニュースのタイトル
    description = models.TextField(blank=True, null=True)  # ニュースの説明
    url = models.URLField()  # ニュースへのリンク
    url_to_image = models.URLField(blank=True, null=True)  # 画像のURL
    published_at = models.DateTimeField()  # 公開日時

    def __str__(self):
        return self.title

class ViewCount(models.Model):
    view_count = models.IntegerField(verbose_name='ビュー数', default=0)

    def __str__(self):
        return str(self.view_count)

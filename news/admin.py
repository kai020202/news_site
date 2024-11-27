from django.contrib import admin
from .models import Post
from .models import ViewCount

admin.site.register(Post)
admin.site.register(ViewCount)

# Register your models here.

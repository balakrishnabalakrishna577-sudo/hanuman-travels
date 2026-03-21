from django.db import models
from django.contrib.auth.models import User


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Blog Categories'


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='blog/')
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    tags = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def reading_time(self):
        word_count = len(self.content.split())
        minutes = max(1, round(word_count / 200))
        return minutes

    class Meta:
        ordering = ['-created_at']

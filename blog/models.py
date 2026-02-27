from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    excerpt = models.CharField(max_length=300, blank=True, verbose_name="خلاصه")
    content = models.TextField(verbose_name="متن مقاله")
    cover_image_url = models.URLField(blank=True, verbose_name="لینک عکس کاور (اختیاری)")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
        verbose_name="نویسنده",
    )

    is_published = models.BooleanField(default=False, verbose_name="منتشر شده؟")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان انتشار")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})

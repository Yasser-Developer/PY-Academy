from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=120, verbose_name="نام")
    contact = models.CharField(max_length=120, blank=True, verbose_name="راه ارتباطی")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده؟")

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"

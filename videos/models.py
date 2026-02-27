from django.conf import settings
from django.db import models


class EducationalVideo(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان ویدیو")
    description = models.TextField(verbose_name="توضیحات")
    youtube_url = models.URLField(blank=True, null=True, verbose_name="لینک یوتیوب (اختیاری)")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="فایل ویدیو mp4 (اختیاری)")
    direct_video_url = models.URLField(blank=True, null=True, verbose_name="لینک مستقیم mp4 (برای پخش داخل سایت)")
    is_english = models.BooleanField(default=False, verbose_name="انگلیسی هست؟")
    subtitle_url = models.URLField(blank=True, null=True, verbose_name="لینک زیرنویس فارسی")
    dubbed_url = models.URLField(blank=True, null=True, verbose_name="لینک دوبله فارسی")
    xp_reward = models.PositiveIntegerField(default=20, verbose_name="جایزه XP")
    min_watch_seconds = models.PositiveIntegerField(default=30, verbose_name="حداقل زمان برای جایزه (ثانیه)")

    def __str__(self):
        return self.title


class WatchedVideo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='watched_videos',
    )
    video = models.ForeignKey(
        EducationalVideo,
        on_delete=models.CASCADE,
        related_name='watch_records',
    )
    watched_at = models.DateTimeField(auto_now_add=True)
    xp_earned = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'video')
        verbose_name = "ویدیوی دیده‌شده"
        verbose_name_plural = "ویدیوهای دیده‌شده"

    def __str__(self):
        return f"{self.user} - {self.video}"
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان دوره")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='courses/', null=True, blank=True, verbose_name="عکس دوره")
    xp_reward = models.PositiveIntegerField(default=200, verbose_name="امتیاز جایزه کل دوره")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_progress(self, user):
        """محاسبه پیشرفت کاربر در این دوره (درصد)"""
        lessons = self.lessons.all()
        completed = user.completed_lessons.filter(lesson__in=lessons).count()
        total = lessons.count()
        return (completed / total * 100) if total > 0 else 0


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="دوره")
    title = models.CharField(max_length=200, verbose_name="عنوان درس")
    content = models.TextField(verbose_name="محتوا (متن یا کد)")
    challenge = models.TextField(blank=True, verbose_name="چالش درس")
    xp_reward = models.PositiveIntegerField(default=50, verbose_name="امتیاز جایزه درس")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "درس‌ها"
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class CompletedLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_lessons')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    xp_earned = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = "درس کامل‌شده"
        verbose_name_plural = "درس‌های کامل‌شده"

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
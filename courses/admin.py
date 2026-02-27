from django.contrib import admin
from .models import Course, Lesson, CompletedLesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'xp_reward', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'xp_reward', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('title', 'content')

@admin.register(CompletedLesson)
class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed_at', 'xp_earned')
    list_filter = ('user', 'lesson__course')
    search_fields = ('user__username', 'lesson__title')
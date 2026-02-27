from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lesson, CompletedLesson, Course


def course_list(request):
    courses = Course.objects.filter(is_active=True)
    context = {
        'courses': courses,
    }
    return render(request, 'courses/course_list.html', context)


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # درس‌های دوره (مرتب‌شده بر اساس order)
    lessons = course.lessons.filter(is_active=True).order_by('order')
    
    # درس‌های کامل‌شده توسط کاربر
    completed_lessons = CompletedLesson.objects.filter(user=request.user, lesson__course=course)
    completed_ids = completed_lessons.values_list('lesson_id', flat=True)
    
    # درصد پیشرفت کاربر در این دوره
    total_lessons = lessons.count()
    completed_count = completed_lessons.count()
    progress = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
    
    context = {
        'course': course,
        'lessons': lessons,
        'completed_ids': completed_ids,
        'progress': progress,
        'completed_count': completed_count,
        'total_lessons': total_lessons,
    }
    return render(request, 'courses/course_detail.html', context)



@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, is_active=True, course__is_active=True)
    
    # چک کن درس قبلاً کامل شده یا نه
    is_completed = CompletedLesson.objects.filter(user=request.user, lesson=lesson).exists()
    
    context = {
        'lesson': lesson,
        'course': lesson.course,
        'is_completed': is_completed,
    }
    
    return render(request, 'courses/lesson_detail.html', context)

@login_required
def complete_lesson(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id, is_active=True)
        
        # چک کن قبلاً کامل نشده باشه
        if not CompletedLesson.objects.filter(user=request.user, lesson=lesson).exists():
            # ثبت درس کامل‌شده
            CompletedLesson.objects.create(
                user=request.user,
                lesson=lesson,
                xp_earned=lesson.xp_reward
            )
            
            # اضافه کردن XP به کاربر
            request.user.add_xp(lesson.xp_reward)
            
            # چک کن آیا همه درس‌های دوره تموم شده
            course = lesson.course
            total_lessons = course.lessons.filter(is_active=True).count()
            completed_lessons = CompletedLesson.objects.filter(
                user=request.user, lesson__course=course
            ).count()
            
            if completed_lessons == total_lessons:
                request.user.add_xp(course.xp_reward)
                messages.success(
                    request,
                    f"دوره '{course.title}' رو کامل کردی! +{course.xp_reward} XP جایزه کل گرفتی! 🎉"
                )
            
            messages.success(
                request,
                f"درس '{lesson.title}' کامل شد! +{lesson.xp_reward} XP گرفتی."
            )
        else:
            messages.info(request, "این درس قبلاً کامل شده بود.")
        
        return redirect('lesson_detail', lesson_id=lesson.id)
    
    return redirect('lesson_detail', lesson_id=lesson.id)
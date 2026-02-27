from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import EducationalVideo, WatchedVideo

def video_list(request):
    videos = EducationalVideo.objects.all()

    watched_ids = []
    if request.user.is_authenticated:
        watched_ids = list(
            WatchedVideo.objects.filter(user=request.user, video__in=videos)
            .values_list('video_id', flat=True)
        )

    return render(
        request,
        'videos/video_list.html',
        {
            'videos': videos,
            'watched_ids': watched_ids,
        },
    )


@login_required
@require_POST
def mark_video_watched(request, video_id):
    video = get_object_or_404(EducationalVideo, pk=video_id)

    record, created = WatchedVideo.objects.get_or_create(
        user=request.user,
        video=video,
        defaults={'xp_earned': video.xp_reward},
    )

    if created:
        request.user.add_xp(video.xp_reward)
        messages.success(request, f"+{video.xp_reward} XP گرفتی! 🎉")
    else:
        messages.info(request, "XP این ویدیو رو قبلاً گرفتی.")

    return redirect(request.META.get('HTTP_REFERER') or 'video_list')
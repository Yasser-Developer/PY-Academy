from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Post


def blog_list(request):
    posts = Post.objects.filter(is_published=True, published_at__lte=timezone.now())
    return render(request, "blog/blog_list.html", {"posts": posts})


def blog_detail(request, slug: str):
    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True,
        published_at__lte=timezone.now(),
    )
    return render(request, "blog/blog_detail.html", {"post": post})

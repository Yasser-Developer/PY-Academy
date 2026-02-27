"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from accounts.views import home, register, user_logout, dashboard, leaderboard, learning_path
from courses.views import course_list, course_detail, lesson_detail, complete_lesson
from games.views import game_list, game_detail, run_game_code
from videos.views import video_list, mark_video_watched
from pages.views import AboutView, FAQView, TermsView, PrivacyView, contact


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),  # داشبورد شخصی
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('learning-path/', learning_path, name='learning_path'),
    path('courses/', course_list, name='course_list'),
    path('courses/<int:course_id>/', course_detail, name='course_detail'),
    path('lessons/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('lessons/<int:lesson_id>/complete/', complete_lesson, name='complete_lesson'),
    path('games/', game_list, name='game_list'),
    path('games/<int:game_id>/', game_detail, name='game_detail'),
    path('games/<int:game_id>/run/', run_game_code, name='run_game_code'),
    path('videos/', video_list, name='video_list'),
    path('videos/<int:video_id>/watched/', mark_video_watched, name='video_mark_watched'),

    path('about/', AboutView.as_view(), name='about'),
    path('contact/', contact, name='contact'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('blog/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
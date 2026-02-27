from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import CustomUser
from blog.models import Post
from courses.models import Course, Lesson
from games.models import GameChallenge
from videos.models import EducationalVideo


class Command(BaseCommand):
    help = "Create starter content (courses/lessons/games/videos/blog posts). Safe to run multiple times."

    @transaction.atomic
    def handle(self, *args, **options):
        now = timezone.now()

        # Ensure at least one staff author for blog posts (optional)
        author = CustomUser.objects.filter(is_staff=True).order_by("id").first()

        course, _ = Course.objects.get_or_create(
            title="پایتون مقدماتی برای بچه‌ها (شروع از صفر)",
            defaults={
                "description": (
                    "این دوره مخصوص شروع از صفره. هر درس کوتاهه و با تمرین و چالش همراهه.\n"
                    "هدف: با مفاهیم پایه پایتون دوست بشی و بتونی برنامه‌های ساده بنویسی."
                ),
                "xp_reward": 200,
                "is_active": True,
            },
        )

        lessons_data = [
            ("سلام پایتون!", "چاپ کردن متن با print", "سلام! اولین برنامه‌ات رو بنویس.", 40),
            ("متغیرها", "چطور اطلاعات رو داخل متغیر نگه داریم", "یک نام و سن داخل متغیرها نگه دار.", 50),
            ("عددها و محاسبه", "جمع و ضرب و تقسیم", "یک ماشین‌حساب ساده بساز.", 50),
            ("رشته‌ها (متن)", "ترکیب متن‌ها و تبدیل عدد به متن", "یک پیام خوشامد بساز.", 50),
            ("شرط‌ها (if)", "تصمیم گرفتن در برنامه", "اگر سن بیشتر از ۱۰ بود پیام بده.", 60),
            ("حلقه‌ها (for)", "تکرار کردن کارها", "از ۱ تا ۱۰ چاپ کن.", 70),
            ("لیست‌ها", "چندتا مقدار را کنار هم نگه داریم", "یک لیست از میوه‌ها بساز و چاپ کن.", 80),
        ]

        for idx, (title, content, challenge, xp) in enumerate(lessons_data, start=1):
            Lesson.objects.get_or_create(
                course=course,
                title=title,
                defaults={
                    "content": f"{content}\n\nمثال:\nprint('سلام دنیا')\n",
                    "challenge": challenge,
                    "xp_reward": xp,
                    "order": idx,
                    "is_active": True,
                },
            )

        games_data = [
            ("حدس عدد", "یک عدد مخفی داریم؛ تلاش کن درست حدس بزنی.", 60),
            ("جمع سریع", "چند عدد رو با هم جمع کن و نتیجه رو چاپ کن.", 40),
            ("لیست امتیازها", "یک لیست از امتیازها بساز و بیشترین رو پیدا کن.", 70),
        ]
        for title, desc, xp in games_data:
            GameChallenge.objects.get_or_create(
                title=title,
                defaults={"description": desc, "xp_reward": xp},
            )

        videos_data = [
            (
                "شروع سریع پایتون برای بچه‌ها",
                "در ۵ دقیقه با print، متغیر و تمرین ساده آشنا شو.",
                "https://www.youtube.com/embed/kqtD5dpn9C8",
                20,
            ),
            (
                "if در پایتون (خیلی ساده)",
                "با شرط‌ها یاد می‌گیری برنامه تصمیم بگیره.",
                "https://www.youtube.com/embed/2C6xO4b7W9o",
                20,
            ),
        ]
        for title, desc, youtube_url, xp in videos_data:
            EducationalVideo.objects.get_or_create(
                title=title,
                defaults={
                    "description": desc,
                    "youtube_url": youtube_url,
                    "xp_reward": xp,
                    "min_watch_seconds": 30,
                },
            )

        posts_data = [
            (
                "چرا پایتون برای بچه‌ها عالیه؟",
                "پایتون ساده، جذاب و مناسب شروع برنامه‌نویسی برای دانش‌آموزهاست.",
                "پایتون به خاطر ساده بودن و خوانایی، برای شروع برنامه‌نویسی عالیه.\n\n"
                "اگر هر روز فقط ۱۵ دقیقه تمرین کنی، خیلی سریع می‌تونی پروژه‌های ساده بسازی.",
                "python-for-kids",
            ),
            (
                "چطور فرزندم رو به کدنویسی علاقه‌مند کنم؟",
                "با بازی، پروژه‌های کوچک و تشویق درست، کدنویسی می‌تونه سرگرم‌کننده بشه.",
                "بهترین راه علاقه‌مند کردن بچه‌ها به کدنویسی اینه که یادگیری رو شبیه بازی کنید.\n\n"
                "پروژه‌های کوتاه، نتیجه سریع و سیستم امتیازدهی کمک می‌کنه ادامه بدن.",
                "motivate-kids-coding",
            ),
        ]
        for title, excerpt, content, slug in posts_data:
            Post.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "excerpt": excerpt,
                    "content": content,
                    "author": author,
                    "is_published": True,
                    "published_at": now,
                },
            )

        self.stdout.write(self.style.SUCCESS("Seed content created/updated successfully."))


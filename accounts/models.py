from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # فیلدهای اضافی
    student_code = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("کد دانش‌آموزی")
    )
    
    xp = models.PositiveIntegerField(
        default=0,
        verbose_name=_("امتیاز تجربه (XP)")
    )
    
    level = models.PositiveSmallIntegerField(
        default=1,
        editable=False,
        verbose_name=_("سطح")
    )
    
    is_vip = models.BooleanField(
        default=False,
        verbose_name=_("عضو ویژه (VIP)")
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name=_("عکس پروفایل")
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_("بیوگرافی")
    )
    
    phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        verbose_name=_("شماره موبایل")
    )
    
    # حل مشکل clash با اضافه کردن related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # ← این خط جدید
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups'),
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # ← این خط جدید
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )
    
    # متدها
    def update_level(self):
        new_level = (self.xp // 100) + 1
        if new_level != self.level:
            self.level = new_level
            self.save(update_fields=['level'])
    
    def add_xp(self, amount: int):
        if amount > 0:
            self.xp += amount
            self.update_level()
            self.save(update_fields=['xp'])
    
    class Meta:
        verbose_name = _("کاربر")
        verbose_name_plural = _("کاربران")
    
    def __str__(self):
        return self.get_full_name() or self.username
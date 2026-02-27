from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'student_code', 'xp', 'level', 'is_vip', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_vip')
    
    # فیلد level رو از fieldsets حذف کن (چون غیرقابل ویرایشه و خودش محاسبه می‌شه)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('اطلاعات شخصی'), {'fields': ('first_name', 'last_name', 'email', 'student_code', 'phone', 'bio', 'avatar')}),
        (_('امتیاز و سطح'), {'fields': ('xp', 'is_vip')}),  # ← level رو اینجا حذف کردیم
        (_('مجوزها'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('تاریخ‌ها'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # در فرم افزودن هم level رو اضافه نکن
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'student_code', 'is_vip'),
        }),
        (_('اطلاعات اضافی'), {'fields': ('xp',)}),
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email', 'student_code')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

# عنوان‌های فارسی پنل
admin.site.site_header = "پنل مدیریت PY-Academy"
admin.site.site_title = "PY-Academy Admin"
admin.site.index_title = "خوش آمدید به مدیریت سایت"
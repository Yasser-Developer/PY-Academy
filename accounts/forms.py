from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'student_code', 'phone', 'avatar')
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-4 rounded-lg bg-gray-800 border border-gray-700 text-[#ffffff] !important placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:text-[#ffffff] !important',
                'placeholder': 'نام کاربری (الزامی)',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-4 rounded-lg bg-gray-800 border border-gray-700 text-[#ffffff] !important placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:text-[#ffffff] !important',
                'placeholder': 'ایمیل (الزامی)',
            }),
            'student_code': forms.TextInput(attrs={
                'class': 'w-full p-4 rounded-lg bg-gray-800 border border-gray-700 text-[#ffffff] !important placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:text-[#ffffff] !important',
                'placeholder': 'کد دانش‌آموزی (اختیاری)',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full p-4 rounded-lg bg-gray-800 border border-gray-700 text-[#ffffff] !important placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:text-[#ffffff] !important',
                'placeholder': 'شماره موبایل (اختیاری)',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full p-4 rounded-lg bg-gray-800 border border-gray-700 text-[#ffffff] !important placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:text-[#ffffff] !important',
                'placeholder': 'رمز عبور (حداقل ۸ کاراکتر)',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full p-4 rounded-lg bg-gray-800 border border-gray-700 text-[#ffffff] !important placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:text-[#ffffff] !important',
                'placeholder': 'تکرار رمز عبور',
            }),
        }

    # متد save برای اضافه کردن XP اولیه
    def save(self, commit=True):
        user = super().save(commit=False)
        user.xp = 50  # هدیه ۵۰ XP برای ثبت‌نام جدید
        user.update_level()  # سطح رو بر اساس XP محاسبه کن
        if commit:
            user.save()
        return user
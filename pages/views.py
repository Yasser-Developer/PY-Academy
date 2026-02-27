from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .models import ContactMessage


class AboutView(TemplateView):
    template_name = "pages/about.html"


class FAQView(TemplateView):
    template_name = "pages/faq.html"


class TermsView(TemplateView):
    template_name = "pages/terms.html"


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"


def contact(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        contact_value = (request.POST.get("contact") or "").strip()
        message_text = (request.POST.get("message") or "").strip()

        if not name or not message_text:
            messages.error(request, "لطفاً نام و پیام را وارد کن.")
            return redirect("contact")

        ContactMessage.objects.create(
            name=name,
            contact=contact_value,
            message=message_text,
        )
        messages.success(request, "پیامت ارسال شد. ممنون! 🙌")
        return redirect("contact")

    return render(request, "pages/contact.html")

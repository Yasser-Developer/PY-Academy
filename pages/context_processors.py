from django.conf import settings


def site_contact(request):
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "PY-Academy"),
        "SITE_TAGLINE": getattr(settings, "SITE_TAGLINE", ""),
        "CONTACT_EMAIL": getattr(settings, "CONTACT_EMAIL", ""),
        "CONTACT_PHONE": getattr(settings, "CONTACT_PHONE", ""),
        "CONTACT_INSTAGRAM": getattr(settings, "CONTACT_INSTAGRAM", ""),
        "CONTACT_TELEGRAM": getattr(settings, "CONTACT_TELEGRAM", ""),
        "CONTACT_ADDRESS": getattr(settings, "CONTACT_ADDRESS", ""),
    }


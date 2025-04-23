from django import template
from django.templatetags.static import static

register = template.Library()

@register.filter
def get_profile_pic_url(profile):
    if profile and profile.profile_pic and profile.profile_pic.name != 'default.jpg':
        return profile.profile_pic.url
    return static('images/default.png')

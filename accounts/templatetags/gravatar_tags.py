# accounts/templatetags/gravatar_tags.py

import hashlib
from django import template

register = template.Library()

@register.filter
def gravatar_url(email, size=40):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s={size}"

# templatetags/category_extras.py
from django import template
from ..models import Category

register = template.Library()

CATEGORY_ICONS = {
    "ادوية البرد": "fas fa-head-side-cough",
    "ادوية القولون": "fas fa-stomach",
    "فيتامينات": "fas fa-capsules",
    # ... باقي التعيينات
}

CATEGORY_COLORS = {
    "ادوية البرد": "#3b82f6",
    "ادوية القولون": "#10b981",
    # ... باقي الألوان
}

CATEGORY_VIEWS = {
    "ادوية البرد": 107801,
    "ادوية القولون": 127041,
    # ... باقي المشاهدات
}

@register.filter
def get_category_icon(category_name):
    return CATEGORY_ICONS.get(category_name, "fas fa-capsules")

@register.filter
def get_category_color(category_name):
    return CATEGORY_COLORS.get(category_name, "#6b7280")

@register.filter
def get_category_views(category_name):
    return CATEGORY_VIEWS.get(category_name, 0)
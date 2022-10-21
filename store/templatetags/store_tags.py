from django import template
from ..models import Category


register = template.Library()

@register.simple_tag()
def get_categories():
    categories = Category.objects.filter(parent=None)
    return categories


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'Narxi bo\'yicha',
            'sorters': 'price'
        },
        {
            'title': 'Nomi bo\'yicha',
            'sorters': 'title'
        },
        {
            'title': 'Vaqti bo\'yicha',
            'sorters': '-created_at'
        }
    ]
    return sorters
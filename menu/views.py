from django.shortcuts import render, get_object_or_404
from .models import Category, MenuItem


def home(request):
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:6]
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'featured_items': featured_items,
        'categories': categories,
    })


def menu_list(request):
    categories = Category.objects.prefetch_related('items').all()
    selected_category = request.GET.get('category', '')
    if selected_category:
        categories = categories.filter(slug=selected_category)
    all_categories = Category.objects.all()
    return render(request, 'menu/menu_list.html', {
        'categories': categories,
        'all_categories': all_categories,
        'selected_category': selected_category,
    })


def menu_detail(request, slug):
    item = get_object_or_404(MenuItem, slug=slug, is_available=True)
    related = MenuItem.objects.filter(category=item.category, is_available=True).exclude(pk=item.pk)[:4]
    return render(request, 'menu/menu_detail.html', {
        'item': item,
        'related': related,
    })

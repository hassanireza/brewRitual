import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from menu.models import MenuItem
from .models import Cart, CartItem, Order, OrderItem
from loyalty.utils import award_loyalty


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


@require_POST
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id, is_available=True)
    cart = get_or_create_cart(request)
    size = request.POST.get('size', 'S')
    qty = int(request.POST.get('quantity', 1))
    special = request.POST.get('special_instructions', '')

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, menu_item=item, size=size,
        defaults={'quantity': qty, 'special_instructions': special}
    )
    if not created:
        cart_item.quantity += qty
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'message': f'{item.name} added to your ritual.',
        })
    messages.success(request, f'{item.name} has been added to your order.')
    return redirect('orders:cart')


@require_POST
def update_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    qty = int(request.POST.get('quantity', 1))
    if qty <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = qty
        cart_item.save()
    return redirect('orders:cart')


@require_POST
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    CartItem.objects.filter(pk=item_id, cart=cart).delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.get_item_count()})
    return redirect('orders:cart')


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('menu:list')

    if request.method == 'POST':
        return process_order(request, cart)

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
@transaction.atomic
def process_order(request, cart):
    use_free_drink = request.POST.get('use_free_drink') == '1'
    notes = request.POST.get('notes', '')

    subtotal = cart.get_total()
    discount = Decimal('0')

    if use_free_drink:
        profile = getattr(request.user, 'loyalty_profile', None)
        if profile and profile.free_drinks_available > 0:
            cheapest = cart.items.order_by('menu_item__price').first()
            if cheapest:
                discount = cheapest.get_unit_price()

    total = max(Decimal('0'), subtotal - discount)

    order_number = f"BR-{uuid.uuid4().hex[:8].upper()}"
    order = Order.objects.create(
        user=request.user,
        order_number=order_number,
        status='confirmed',
        payment_status='paid',
        subtotal=subtotal,
        total=total,
        notes=notes,
    )

    for ci in cart.items.all():
        OrderItem.objects.create(
            order=order,
            menu_item=ci.menu_item,
            item_name=ci.menu_item.name,
            quantity=ci.quantity,
            size=ci.size,
            unit_price=ci.get_unit_price(),
            subtotal=ci.get_subtotal(),
            special_instructions=ci.special_instructions,
        )

    award_loyalty(request.user, order, used_free_drink=use_free_drink and discount > 0)
    cart.items.all().delete()

    messages.success(request, f'Order #{order_number} placed. Your ritual begins!')
    return redirect('orders:order_detail', order_number=order_number)


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

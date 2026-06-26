"""
Brew Ritual - Full Test Suite
Run with: python manage.py test tests
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from menu.models import Category, MenuItem
from orders.models import Cart, CartItem, Order, OrderItem
from loyalty.models import LoyaltyProfile, LoyaltyTransaction
from loyalty.utils import get_or_create_profile, award_loyalty
from accounts.models import UserProfile


def make_user(username='testuser', password='testpass123'):
    user = User.objects.create_user(username=username, email=f'{username}@test.com', password=password)
    UserProfile.objects.get_or_create(user=user)
    get_or_create_profile(user)
    return user


def make_category():
    return Category.objects.create(name='Espresso', slug='espresso-test', order=1)


def make_item(category, slug='test-espresso', price='3.50', featured=False):
    return MenuItem.objects.create(
        category=category, name='Test Espresso', slug=slug,
        description='A test coffee item.', price=Decimal(price),
        is_available=True, is_featured=featured, is_loyalty_eligible=True,
    )


# ─── PAGE LOAD TESTS ──────────────────────────────────────────────────────────

class PublicPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = make_category()
        self.item = make_item(self.cat)

    def test_home_loads(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Brew Ritual')

    def test_menu_list_loads(self):
        r = self.client.get(reverse('menu:list'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test Espresso')

    def test_menu_detail_loads(self):
        r = self.client.get(reverse('menu:detail', args=[self.item.slug]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test Espresso')

    def test_menu_detail_404(self):
        r = self.client.get(reverse('menu:detail', args=['nonexistent-item']))
        self.assertEqual(r.status_code, 404)

    def test_ritual_guide_loads(self):
        r = self.client.get(reverse('ritual:home'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Ritual Guide')

    def test_login_page_loads(self):
        r = self.client.get(reverse('accounts:login'))
        self.assertEqual(r.status_code, 200)

    def test_register_page_loads(self):
        r = self.client.get(reverse('accounts:register'))
        self.assertEqual(r.status_code, 200)

    def test_cart_loads_for_anonymous(self):
        r = self.client.get(reverse('orders:cart'))
        self.assertEqual(r.status_code, 200)

    def test_checkout_redirects_unauthenticated(self):
        r = self.client.get(reverse('orders:checkout'))
        self.assertRedirects(r, '/accounts/login/?next=/orders/checkout/', fetch_redirect_response=False)

    def test_loyalty_requires_login(self):
        r = self.client.get(reverse('loyalty:dashboard'))
        self.assertEqual(r.status_code, 302)

    def test_menu_filter_by_category(self):
        r = self.client.get(reverse('menu:list') + '?category=espresso-test')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test Espresso')


# ─── AUTH TESTS ───────────────────────────────────────────────────────────────

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_creates_user(self):
        r = self.client.post(reverse('accounts:register'), {
            'username': 'newuser', 'email': 'new@test.com',
            'password1': 'securepass123', 'password2': 'securepass123',
            'first_name': 'New',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(r, '/', fetch_redirect_response=False)

    def test_register_creates_loyalty_profile(self):
        self.client.post(reverse('accounts:register'), {
            'username': 'loyaluser', 'email': 'loyal@test.com',
            'password1': 'securepass123', 'password2': 'securepass123',
        })
        user = User.objects.get(username='loyaluser')
        self.assertTrue(LoyaltyProfile.objects.filter(user=user).exists())

    def test_register_gives_welcome_points(self):
        self.client.post(reverse('accounts:register'), {
            'username': 'pointsuser', 'email': 'pts@test.com',
            'password1': 'securepass123', 'password2': 'securepass123',
        })
        user = User.objects.get(username='pointsuser')
        profile = LoyaltyProfile.objects.get(user=user)
        self.assertEqual(profile.total_points, 20)

    def test_register_password_mismatch(self):
        r = self.client.post(reverse('accounts:register'), {
            'username': 'baduser', 'email': 'bad@test.com',
            'password1': 'pass1', 'password2': 'pass2',
        })
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_login_valid_credentials(self):
        user = make_user('loginuser', 'pass123word')
        r = self.client.post(reverse('accounts:login'), {
            'username': 'loginuser', 'password': 'pass123word',
        })
        self.assertRedirects(r, '/', fetch_redirect_response=False)

    def test_login_invalid_credentials(self):
        make_user('loginuser2')
        r = self.client.post(reverse('accounts:login'), {
            'username': 'loginuser2', 'password': 'wrongpassword',
        })
        self.assertEqual(r.status_code, 200)

    def test_logout_redirects(self):
        user = make_user('logoutuser')
        self.client.force_login(user)
        r = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(r, '/', fetch_redirect_response=False)

    def test_profile_requires_login(self):
        r = self.client.get(reverse('accounts:profile'))
        self.assertEqual(r.status_code, 302)

    def test_profile_loads_for_authenticated(self):
        user = make_user()
        self.client.force_login(user)
        r = self.client.get(reverse('accounts:profile'))
        self.assertEqual(r.status_code, 200)

    def test_profile_update(self):
        user = make_user()
        self.client.force_login(user)
        self.client.post(reverse('accounts:profile'), {
            'first_name': 'Updated', 'last_name': 'Name',
            'email': 'updated@test.com', 'phone': '07700000000', 'bio': 'Coffee lover',
        })
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')


# ─── MENU TESTS ───────────────────────────────────────────────────────────────

class MenuModelTests(TestCase):
    def setUp(self):
        self.cat = make_category()
        self.item = MenuItem.objects.create(
            category=self.cat, name='Size Test', slug='size-test',
            description='Has sizes', price=Decimal('3.50'),
            price_medium=Decimal('4.00'), price_large=Decimal('4.50'),
        )

    def test_item_str(self):
        self.assertEqual(str(self.item), 'Size Test')

    def test_price_for_small(self):
        self.assertEqual(self.item.get_price_for_size('S'), Decimal('3.50'))

    def test_price_for_medium(self):
        self.assertEqual(self.item.get_price_for_size('M'), Decimal('4.00'))

    def test_price_for_large(self):
        self.assertEqual(self.item.get_price_for_size('L'), Decimal('4.50'))

    def test_has_sizes_true(self):
        self.assertTrue(self.item.has_sizes())

    def test_has_sizes_false(self):
        item2 = make_item(self.cat, 'no-size-item')
        self.assertFalse(item2.has_sizes())

    def test_flavor_list_parsing(self):
        item = make_item(self.cat, 'flavor-item')
        item.flavor_notes = 'Chocolate, Caramel, Vanilla'
        item.save()
        self.assertEqual(item.flavor_list, ['Chocolate', 'Caramel', 'Vanilla'])

    def test_unavailable_item_not_in_detail(self):
        item = make_item(self.cat, 'unavailable-item')
        item.is_available = False
        item.save()
        r = self.client.get(reverse('menu:detail', args=['unavailable-item']))
        self.assertEqual(r.status_code, 404)

    def test_featured_on_home(self):
        item = make_item(self.cat, 'featured-test', featured=True)
        r = self.client.get('/')
        self.assertContains(r, 'Test Espresso')


# ─── CART TESTS ───────────────────────────────────────────────────────────────

class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = make_user()
        self.cat = make_category()
        self.item = make_item(self.cat)

    def test_add_to_cart_logged_in(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse('orders:add_to_cart', args=[self.item.pk]), {
            'size': 'S', 'quantity': 1,
        })
        self.assertEqual(r.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.get_item_count(), 1)

    def test_add_to_cart_increases_quantity(self):
        self.client.force_login(self.user)
        url = reverse('orders:add_to_cart', args=[self.item.pk])
        self.client.post(url, {'size': 'S', 'quantity': 2})
        self.client.post(url, {'size': 'S', 'quantity': 1})
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.get_item_count(), 3)

    def test_cart_total_correct(self):
        self.client.force_login(self.user)
        self.client.post(reverse('orders:add_to_cart', args=[self.item.pk]), {
            'size': 'S', 'quantity': 2,
        })
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.get_total(), Decimal('7.00'))

    def test_remove_from_cart(self):
        self.client.force_login(self.user)
        self.client.post(reverse('orders:add_to_cart', args=[self.item.pk]), {'size': 'S', 'quantity': 1})
        cart = Cart.objects.get(user=self.user)
        ci = cart.items.first()
        self.client.post(reverse('orders:remove_from_cart', args=[ci.pk]))
        self.assertEqual(cart.get_item_count(), 0)

    def test_update_cart_quantity(self):
        self.client.force_login(self.user)
        self.client.post(reverse('orders:add_to_cart', args=[self.item.pk]), {'size': 'S', 'quantity': 1})
        cart = Cart.objects.get(user=self.user)
        ci = cart.items.first()
        self.client.post(reverse('orders:update_cart', args=[ci.pk]), {'quantity': 3})
        ci.refresh_from_db()
        self.assertEqual(ci.quantity, 3)

    def test_update_cart_zero_removes_item(self):
        self.client.force_login(self.user)
        self.client.post(reverse('orders:add_to_cart', args=[self.item.pk]), {'size': 'S', 'quantity': 1})
        cart = Cart.objects.get(user=self.user)
        ci = cart.items.first()
        self.client.post(reverse('orders:update_cart', args=[ci.pk]), {'quantity': 0})
        self.assertFalse(CartItem.objects.filter(pk=ci.pk).exists())

    def test_anonymous_add_to_cart(self):
        session = self.client.session
        session.save()
        r = self.client.post(reverse('orders:add_to_cart', args=[self.item.pk]), {'size': 'S', 'quantity': 1})
        self.assertEqual(r.status_code, 302)

    def test_ajax_add_to_cart_returns_json(self):
        self.client.force_login(self.user)
        r = self.client.post(
            reverse('orders:add_to_cart', args=[self.item.pk]),
            {'size': 'S', 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data['success'])
        self.assertIn('cart_count', data)


# ─── ORDER TESTS ──────────────────────────────────────────────────────────────

class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = make_user()
        self.cat = make_category()
        self.item = make_item(self.cat)

    def _add_item_and_checkout(self, use_free=False):
        self.client.force_login(self.user)
        self.client.post(reverse('orders:add_to_cart', args=[self.item.pk]), {'size': 'S', 'quantity': 1})
        data = {'notes': 'Test order'}
        if use_free:
            data['use_free_drink'] = '1'
        return self.client.post(reverse('orders:checkout'), data)

    def test_checkout_creates_order(self):
        self._add_item_and_checkout()
        self.assertEqual(Order.objects.filter(user=self.user).count(), 1)

    def test_order_has_correct_total(self):
        self._add_item_and_checkout()
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total, Decimal('3.50'))

    def test_checkout_clears_cart(self):
        self._add_item_and_checkout()
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.get_item_count(), 0)

    def test_order_detail_accessible(self):
        self._add_item_and_checkout()
        order = Order.objects.get(user=self.user)
        r = self.client.get(reverse('orders:order_detail', args=[order.order_number]))
        self.assertEqual(r.status_code, 200)

    def test_order_detail_restricted_to_owner(self):
        self._add_item_and_checkout()
        order = Order.objects.get(user=self.user)
        other = make_user('otheruser')
        self.client.force_login(other)
        r = self.client.get(reverse('orders:order_detail', args=[order.order_number]))
        self.assertEqual(r.status_code, 404)

    def test_order_history_loads(self):
        self._add_item_and_checkout()
        r = self.client.get(reverse('orders:history'))
        self.assertEqual(r.status_code, 200)

    def test_checkout_requires_login(self):
        r = self.client.get(reverse('orders:checkout'))
        self.assertEqual(r.status_code, 302)

    def test_checkout_redirects_empty_cart(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse('orders:checkout'), {'notes': ''})
        self.assertEqual(r.status_code, 302)

    def test_order_number_format(self):
        self._add_item_and_checkout()
        order = Order.objects.get(user=self.user)
        self.assertTrue(order.order_number.startswith('BR-'))
        self.assertEqual(len(order.order_number), 11)

    def test_order_items_created(self):
        self._add_item_and_checkout()
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.items.count(), 1)
        oi = order.items.first()
        self.assertEqual(oi.item_name, 'Test Espresso')


# ─── LOYALTY TESTS ────────────────────────────────────────────────────────────

class LoyaltyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = make_user()
        self.profile = get_or_create_profile(self.user)

    def test_profile_created_on_register(self):
        self.assertIsNotNone(self.profile)

    def test_welcome_points(self):
        self.assertEqual(self.profile.total_points, 20)

    def test_welcome_transaction_exists(self):
        self.assertTrue(
            LoyaltyTransaction.objects.filter(profile=self.profile, transaction_type='welcome').exists()
        )

    def test_dashboard_loads(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse('loyalty:dashboard'))
        self.assertEqual(r.status_code, 200)

    def test_order_awards_points(self):
        cat = make_category()
        item = make_item(cat)
        order = Order.objects.create(
            user=self.user, order_number='BR-TEST0001',
            status='confirmed', payment_status='paid',
            subtotal=Decimal('3.50'), total=Decimal('3.50'),
        )
        OrderItem.objects.create(
            order=order, menu_item=item, item_name=item.name,
            quantity=1, size='S', unit_price=Decimal('3.50'), subtotal=Decimal('3.50'),
        )
        initial_points = self.profile.total_points
        award_loyalty(self.user, order)
        self.profile.refresh_from_db()
        self.assertGreater(self.profile.total_points, initial_points)

    def test_order_awards_stamp(self):
        cat = make_category()
        item = make_item(cat)
        order = Order.objects.create(
            user=self.user, order_number='BR-TEST0002',
            status='confirmed', payment_status='paid',
            subtotal=Decimal('3.50'), total=Decimal('3.50'),
        )
        OrderItem.objects.create(
            order=order, menu_item=item, item_name=item.name,
            quantity=1, size='S', unit_price=Decimal('3.50'), subtotal=Decimal('3.50'),
        )
        initial_stamps = self.profile.stamps
        award_loyalty(self.user, order)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.stamps, initial_stamps + 1)

    def test_ten_stamps_gives_free_drink(self):
        cat = make_category()
        item = make_item(cat)
        self.profile.stamps = 9
        self.profile.save()
        order = Order.objects.create(
            user=self.user, order_number='BR-TEST0003',
            status='confirmed', payment_status='paid',
            subtotal=Decimal('3.50'), total=Decimal('3.50'),
        )
        OrderItem.objects.create(
            order=order, menu_item=item, item_name=item.name,
            quantity=1, size='S', unit_price=Decimal('3.50'), subtotal=Decimal('3.50'),
        )
        award_loyalty(self.user, order)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.free_drinks_available, 1)
        self.assertEqual(self.profile.stamps, 0)

    def test_tier_bronze_default(self):
        self.assertEqual(self.profile.tier, 'bronze')

    def test_tier_upgrades_to_silver(self):
        self.profile.lifetime_points = 100
        self.profile.update_tier()
        self.assertEqual(self.profile.tier, 'silver')

    def test_tier_upgrades_to_gold(self):
        self.profile.lifetime_points = 300
        self.profile.update_tier()
        self.assertEqual(self.profile.tier, 'gold')

    def test_tier_upgrades_to_platinum(self):
        self.profile.lifetime_points = 700
        self.profile.update_tier()
        self.assertEqual(self.profile.tier, 'platinum')

    def test_stamps_progress_pct(self):
        self.profile.stamps = 5
        self.profile.save()
        self.assertEqual(self.profile.stamps_progress_pct(), 50)

    def test_stamps_remaining(self):
        self.profile.stamps = 3
        self.profile.save()
        self.assertEqual(self.profile.stamps_remaining(), 7)

    def test_next_tier_info_bronze(self):
        info = self.profile.next_tier_info()
        self.assertIsNotNone(info)
        self.assertEqual(info['tier'], 'silver')

    def test_next_tier_info_platinum_is_none(self):
        self.profile.tier = 'platinum'
        self.profile.save()
        info = self.profile.next_tier_info()
        self.assertIsNone(info)

    def test_total_orders_increments(self):
        cat = make_category()
        item = make_item(cat, 'orders-count-item')
        order = Order.objects.create(
            user=self.user, order_number='BR-TEST0004',
            status='confirmed', payment_status='paid',
            subtotal=Decimal('3.50'), total=Decimal('3.50'),
        )
        OrderItem.objects.create(
            order=order, menu_item=item, item_name=item.name,
            quantity=1, size='S', unit_price=Decimal('3.50'), subtotal=Decimal('3.50'),
        )
        award_loyalty(self.user, order)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.total_orders, 1)


# ─── CONTEXT PROCESSOR TESTS ──────────────────────────────────────────────────

class ContextProcessorTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cart_count_in_context(self):
        r = self.client.get('/')
        self.assertIn('cart_count', r.context)

    def test_loyalty_status_anonymous(self):
        r = self.client.get('/')
        self.assertIn('loyalty_tier', r.context)
        self.assertIsNone(r.context['loyalty_tier'])

    def test_loyalty_status_logged_in(self):
        user = make_user()
        self.client.force_login(user)
        r = self.client.get('/')
        self.assertIn('loyalty_tier', r.context)
        self.assertEqual(r.context['loyalty_tier'], 'bronze')

from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user or self.session_key}"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    SIZE_CHOICES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='S')
    special_instructions = models.CharField(max_length=300, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_unit_price(self):
        return self.menu_item.get_price_for_size(self.size)

    def get_subtotal(self):
        return self.get_unit_price() * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} ({self.size})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    stripe_payment_intent = models.CharField(max_length=200, blank=True)
    loyalty_stamps_earned = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number}"


class OrderItem(models.Model):
    SIZE_CHOICES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='S')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    special_instructions = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.item_name}"

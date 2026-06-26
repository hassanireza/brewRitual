from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class LoyaltyProfile(models.Model):
    TIER_CHOICES = [
        ('bronze', 'Bronze Brewer'),
        ('silver', 'Silver Ritualist'),
        ('gold', 'Gold Alchemist'),
        ('platinum', 'Platinum Maestro'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loyalty_profile')
    total_points = models.PositiveIntegerField(default=0)
    lifetime_points = models.PositiveIntegerField(default=0)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='bronze')
    stamps = models.PositiveIntegerField(default=0, help_text="Stamps toward next free drink")
    total_stamps_earned = models.PositiveIntegerField(default=0)
    free_drinks_available = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_tier_display()}"

    def stamps_per_free(self):
        return getattr(settings, 'LOYALTY_STAMPS_PER_FREE', 10)

    def stamps_progress_pct(self):
        return int((self.stamps / self.stamps_per_free()) * 100)

    def stamps_remaining(self):
        return self.stamps_per_free() - self.stamps

    def next_tier_info(self):
        thresholds = {
            'bronze': ('silver', settings.LOYALTY_POINTS_FOR_TIER_SILVER),
            'silver': ('gold', settings.LOYALTY_POINTS_FOR_TIER_GOLD),
            'gold': ('platinum', settings.LOYALTY_POINTS_FOR_TIER_PLATINUM),
            'platinum': (None, None),
        }
        next_tier, threshold = thresholds.get(self.tier, (None, None))
        if threshold:
            remaining = max(0, threshold - self.lifetime_points)
            progress = min(100, int((self.lifetime_points / threshold) * 100))
            return {'tier': next_tier, 'threshold': threshold, 'remaining': remaining, 'progress': progress}
        return None

    def update_tier(self):
        pts = self.lifetime_points
        s = getattr(settings, 'LOYALTY_POINTS_FOR_TIER_SILVER', 100)
        g = getattr(settings, 'LOYALTY_POINTS_FOR_TIER_GOLD', 300)
        p = getattr(settings, 'LOYALTY_POINTS_FOR_TIER_PLATINUM', 700)
        if pts >= p:
            self.tier = 'platinum'
        elif pts >= g:
            self.tier = 'gold'
        elif pts >= s:
            self.tier = 'silver'
        else:
            self.tier = 'bronze'


class LoyaltyTransaction(models.Model):
    TYPE_CHOICES = [
        ('earn_order', 'Points Earned from Order'),
        ('earn_stamp', 'Stamp Earned'),
        ('redeem_drink', 'Free Drink Redeemed'),
        ('redeem_points', 'Points Redeemed'),
        ('tier_bonus', 'Tier Bonus'),
        ('welcome', 'Welcome Bonus'),
    ]

    profile = models.ForeignKey(LoyaltyProfile, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    points = models.IntegerField(default=0)
    stamps = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    order_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.profile.user.username} - {self.get_transaction_type_display()}"

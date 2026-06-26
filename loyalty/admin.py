from django.contrib import admin
from .models import LoyaltyProfile, LoyaltyTransaction

@admin.register(LoyaltyProfile)
class LoyaltyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier', 'total_points', 'stamps', 'free_drinks_available']

@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ['profile', 'transaction_type', 'points', 'stamps', 'created_at']

from django.conf import settings
from .models import LoyaltyProfile, LoyaltyTransaction


def get_or_create_profile(user):
    profile, created = LoyaltyProfile.objects.get_or_create(user=user)
    if created:
        LoyaltyTransaction.objects.create(
            profile=profile,
            transaction_type='welcome',
            points=20,
            stamps=0,
            description='Welcome to the Brew Ritual family. 20 bonus points to start your journey.',
        )
        profile.total_points = 20
        profile.lifetime_points = 20
        profile.save()
    return profile


def award_loyalty(user, order, used_free_drink=False):
    profile = get_or_create_profile(user)

    points_per_order = getattr(settings, 'LOYALTY_POINTS_PER_ORDER', 10)
    stamps_per_free = getattr(settings, 'LOYALTY_STAMPS_PER_FREE', 10)

    eligible_items = order.items.filter(menu_item__is_loyalty_eligible=True)
    eligible_count = sum(i.quantity for i in eligible_items)

    profile.total_orders += 1
    profile.total_points += points_per_order
    profile.lifetime_points += points_per_order

    LoyaltyTransaction.objects.create(
        profile=profile,
        transaction_type='earn_order',
        points=points_per_order,
        description=f'Points earned from order #{order.order_number}',
        order_number=order.order_number,
    )

    for _ in range(eligible_count):
        profile.stamps += 1
        profile.total_stamps_earned += 1

        LoyaltyTransaction.objects.create(
            profile=profile,
            transaction_type='earn_stamp',
            stamps=1,
            description=f'Stamp earned from order #{order.order_number}',
            order_number=order.order_number,
        )

        if profile.stamps >= stamps_per_free:
            profile.stamps -= stamps_per_free
            profile.free_drinks_available += 1
            LoyaltyTransaction.objects.create(
                profile=profile,
                transaction_type='redeem_drink',
                description=f'Free drink unlocked after {stamps_per_free} stamps!',
                order_number=order.order_number,
            )

    if used_free_drink:
        profile.free_drinks_available = max(0, profile.free_drinks_available - 1)
        LoyaltyTransaction.objects.create(
            profile=profile,
            transaction_type='redeem_drink',
            description=f'Free drink redeemed on order #{order.order_number}',
            order_number=order.order_number,
        )

    order.loyalty_stamps_earned = eligible_count
    order.save(update_fields=['loyalty_stamps_earned'])

    profile.update_tier()
    profile.save()

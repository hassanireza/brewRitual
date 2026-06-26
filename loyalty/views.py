from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_or_create_profile


@login_required
def loyalty_dashboard(request):
    profile = get_or_create_profile(request.user)
    transactions = profile.transactions.all()[:20]
    next_tier = profile.next_tier_info()
    stamps_per_free = profile.stamps_per_free()
    stamp_range = range(stamps_per_free)
    filled_stamps = range(profile.stamps)

    tier_perks = {
        'bronze': ['1 stamp per eligible drink', 'Welcome bonus 20 points', 'Free drink every 10 stamps'],
        'silver': ['Priority order processing', '1.25x points multiplier', 'Monthly double-stamp weekend'],
        'gold': ['1.5x points multiplier', 'Early access to seasonal menus', 'Complimentary size upgrade once a week'],
        'platinum': ['2x points multiplier', 'Reserved barista consultation', 'Annual Ritual Box gift', 'Exclusive blend previews'],
    }

    return render(request, 'loyalty/dashboard.html', {
        'profile': profile,
        'transactions': transactions,
        'next_tier': next_tier,
        'stamps_per_free': stamps_per_free,
        'stamp_range': stamp_range,
        'filled_stamps': profile.stamps,
        'tier_perks': tier_perks.get(profile.tier, []),
        'all_tier_perks': tier_perks,
    })

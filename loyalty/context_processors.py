def loyalty_status(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.loyalty_profile
            return {
                'loyalty_tier': profile.tier,
                'loyalty_stamps': profile.stamps,
                'loyalty_free_drinks': profile.free_drinks_available,
            }
        except Exception:
            pass
    return {'loyalty_tier': None, 'loyalty_stamps': 0, 'loyalty_free_drinks': 0}

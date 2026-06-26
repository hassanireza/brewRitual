from django.shortcuts import render


MACHINES = [
    {
        'id': 'espresso',
        'name': 'Espresso Machine',
        'desc': 'The crown jewel of coffee craft. Pressurized hot water meets finely ground beans to produce concentrated liquid gold.',
        'pressure': '9 bar',
        'temp': '90-96C',
        'grind': 'Fine',
        'coffees': ['espresso', 'doppio', 'americano', 'cappuccino', 'latte', 'flat_white', 'macchiato', 'cortado', 'mocha', 'lungo'],
    },
    {
        'id': 'moka',
        'name': 'Moka Pot',
        'desc': 'The stovetop icon. Steam pressure brews rich, bold coffee with an intensity that bridges espresso and drip.',
        'pressure': '1-2 bar',
        'temp': '100C',
        'grind': 'Medium-Fine',
        'coffees': ['moka_coffee', 'moka_latte', 'cafe_au_lait'],
    },
    {
        'id': 'pour_over',
        'name': 'Pour Over',
        'desc': 'Patience as practice. Slow, deliberate pouring reveals every nuance of origin, roast, and terroir.',
        'pressure': 'Gravity',
        'temp': '92-96C',
        'grind': 'Medium',
        'coffees': ['pour_over', 'iced_pour_over', 'pour_over_latte'],
    },
    {
        'id': 'french_press',
        'name': 'French Press',
        'desc': 'Full immersion. No paper filter means a full-bodied, oil-rich cup that coffee purists swear by.',
        'pressure': 'None',
        'temp': '93-96C',
        'grind': 'Coarse',
        'coffees': ['french_press', 'french_press_latte', 'cold_brew_fp'],
    },
    {
        'id': 'aeropress',
        'name': 'AeroPress',
        'desc': 'The traveler\'s alchemist kit. Versatile, forgiving, and capable of producing remarkably clean cups.',
        'pressure': 'Manual',
        'temp': '80-96C',
        'grind': 'Fine-Medium',
        'coffees': ['aeropress_espresso', 'aeropress_latte', 'aeropress_cold'],
    },
    {
        'id': 'cold_brew',
        'name': 'Cold Brew Tower',
        'desc': 'Time is the ingredient. 12 to 24 hours of cold extraction yields a smooth, low-acid concentrate unlike anything else.',
        'pressure': 'None',
        'temp': '4C (Cold)',
        'grind': 'Extra Coarse',
        'coffees': ['cold_brew_straight', 'cold_brew_milk', 'nitro_cold_brew'],
    },
]


def ritual_home(request):
    return render(request, 'ritual_guide/home.html', {'machines': MACHINES})

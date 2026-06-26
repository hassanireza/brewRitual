from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from menu.models import Category, MenuItem

ESPRESSO_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="55" cy="82" rx="32" ry="6" fill="#C8954A" opacity="0.2"/>
  <path d="M30 62 L33 80 Q33 83 36 83 L74 83 Q77 83 77 80 L80 62 Z" fill="#1C0F0A" opacity="0.9"/>
  <path d="M29 59 Q29 57 31 57 L79 57 Q81 57 81 59 L81 62 L29 62 Z" fill="#C8954A" opacity="0.85"/>
  <ellipse cx="55" cy="57" rx="26" ry="4" fill="#C8954A" opacity="0.4"/>
  <path d="M80 64 Q92 64 92 70 Q92 76 80 75" stroke="#C8954A" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M42 52 Q44 44 42 36" stroke="#EDD9B8" stroke-width="2" fill="none" stroke-linecap="round" class="steam-path" opacity="0.75"/>
  <path d="M55 54 Q57 46 55 38" stroke="#EDD9B8" stroke-width="2" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.35s" opacity="0.75"/>
  <path d="M68 52 Q70 44 68 36" stroke="#EDD9B8" stroke-width="2" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.7s" opacity="0.75"/>
  <ellipse cx="55" cy="65" rx="18" ry="5" fill="#C8954A" opacity="0.25"/>
</svg>'''

CAPPUCCINO_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="55" cy="84" rx="30" ry="5" fill="#C8954A" opacity="0.2"/>
  <path d="M26 60 L30 80 Q30 83 33 83 L77 83 Q80 83 80 80 L84 60 Z" fill="#2E1A10" opacity="0.9"/>
  <ellipse cx="55" cy="60" rx="29" ry="9" fill="#F8F0DC"/>
  <ellipse cx="55" cy="58" rx="22" ry="7" fill="#EDD9B8"/>
  <path d="M38 58 Q45 52 55 56 Q65 60 72 55" stroke="#C8954A" stroke-width="1.5" fill="none" opacity="0.6" stroke-linecap="round"/>
  <path d="M80 63 Q91 63 91 69 Q91 75 80 74" stroke="#C8954A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M40 50 Q42 43 40 36" stroke="#EDD9B8" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" opacity="0.65"/>
  <path d="M55 52 Q57 45 55 38" stroke="#EDD9B8" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.3s" opacity="0.65"/>
  <path d="M70 50 Q72 43 70 36" stroke="#EDD9B8" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.6s" opacity="0.65"/>
</svg>'''

LATTE_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="55" cy="87" rx="28" ry="5" fill="#C8954A" opacity="0.18"/>
  <path d="M22 52 L27 80 Q27 84 31 84 L79 84 Q83 84 83 80 L88 52 Z" fill="#EDD9B8" opacity="0.15"/>
  <path d="M24 50 L29 78 Q29 82 33 82 L77 82 Q81 82 81 78 L86 50 Z" fill="#2E1A10"/>
  <ellipse cx="55" cy="58" rx="26" ry="8" fill="#E8C17A" opacity="0.9"/>
  <path d="M36 56 Q44 48 55 54 Q66 60 74 53" stroke="white" stroke-width="1.5" fill="none" opacity="0.5" stroke-linecap="round"/>
  <ellipse cx="55" cy="56" rx="10" ry="3" fill="white" opacity="0.3"/>
  <path d="M42 44 Q44 37 42 30" stroke="#EDD9B8" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" opacity="0.6"/>
  <path d="M55 46 Q57 39 55 32" stroke="#EDD9B8" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.35s" opacity="0.6"/>
  <path d="M68 44 Q70 37 68 30" stroke="#EDD9B8" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.7s" opacity="0.6"/>
</svg>'''

COLD_BREW_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="28" y="22" width="54" height="66" rx="8" fill="#1C0F0A" opacity="0.9"/>
  <rect x="30" y="24" width="50" height="62" rx="7" fill="#2A1410"/>
  <rect x="30" y="52" width="50" height="34" rx="0" fill="#1C0F0A" opacity="0.95"/>
  <rect x="30" y="52" width="50" height="8" fill="#3D2010"/>
  <path d="M34 42 Q55 36 76 42" stroke="#5C3D28" stroke-width="1" fill="none" opacity="0.5"/>
  <path d="M34 48 Q55 44 76 48" stroke="#5C3D28" stroke-width="1" fill="none" opacity="0.5"/>
  <rect x="42" y="16" width="26" height="8" rx="4" fill="#5C3D28"/>
  <circle cx="45" cy="64" r="3" fill="#4A8FBE" opacity="0.7"/>
  <circle cx="58" cy="70" r="2.5" fill="#5A9FCE" opacity="0.6"/>
  <circle cx="66" cy="61" r="2" fill="#4A8FBE" opacity="0.5"/>
  <circle cx="50" cy="75" r="2" fill="#5A9FCE" opacity="0.5"/>
  <ellipse cx="55" cy="88" rx="24" ry="5" fill="#C8954A" opacity="0.15"/>
</svg>'''

POUR_OVER_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M20 30 L55 80 L90 30 Z" fill="none" stroke="#C8954A" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M28 30 L55 80 L82 30 Z" fill="#C8954A" opacity="0.15"/>
  <path d="M50 56 Q55 52 60 56" stroke="#C8954A" stroke-width="1.5" fill="none" opacity="0.6"/>
  <rect x="45" y="80" width="20" height="5" rx="2" fill="#E8C17A" opacity="0.6"/>
  <ellipse cx="55" cy="92" rx="22" ry="6" fill="#1C0F0A" opacity="0.8"/>
  <ellipse cx="55" cy="92" rx="18" ry="4.5" fill="#2E1A10"/>
  <path d="M15 30 L95 30" stroke="#5C3D28" stroke-width="2" stroke-linecap="round"/>
  <path d="M50 22 Q55 10 60 22" stroke="#EDD9B8" stroke-width="2" fill="none" stroke-linecap="round" class="steam-path" opacity="0.6"/>
</svg>'''

FRENCH_PRESS_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="28" width="50" height="56" rx="5" fill="none" stroke="#C8954A" stroke-width="2"/>
  <rect x="32" y="30" width="46" height="52" rx="4" fill="#2A1410" opacity="0.9"/>
  <rect x="32" y="52" width="46" height="30" rx="0" fill="#3D2010" opacity="0.8"/>
  <path d="M34 52 L76 52" stroke="#C8954A" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="55" cy="52" r="5" fill="#C8954A" opacity="0.5"/>
  <circle cx="55" cy="52" r="2.5" fill="#C8954A"/>
  <path d="M53 20 L53 28 L57 28 L57 20" fill="#E8C17A" opacity="0.5" stroke="#C8954A" stroke-width="1"/>
  <rect x="28" y="82" width="54" height="5" rx="2.5" fill="#E8C17A" opacity="0.4"/>
  <ellipse cx="55" cy="87" rx="24" ry="4" fill="#C8954A" opacity="0.15"/>
  <path d="M42 42 Q44 35 42 28" stroke="#EDD9B8" stroke-width="1.5" fill="none" stroke-linecap="round" class="steam-path" opacity="0.6"/>
  <path d="M55 44 Q57 37 55 30" stroke="#EDD9B8" stroke-width="1.5" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.35s" opacity="0.6"/>
  <path d="M68 42 Q70 35 68 28" stroke="#EDD9B8" stroke-width="1.5" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.7s" opacity="0.6"/>
</svg>'''

MATCHA_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="55" cy="84" rx="30" ry="6" fill="#7A8C6E" opacity="0.2"/>
  <path d="M26 60 L30 80 Q30 83 33 83 L77 83 Q80 83 80 80 L84 60 Z" fill="#2E3D28" opacity="0.9"/>
  <ellipse cx="55" cy="60" rx="29" ry="9" fill="#7A8C6E" opacity="0.9"/>
  <ellipse cx="55" cy="59" rx="22" ry="7" fill="#8A9C7E"/>
  <path d="M40 58 Q48 52 55 56 Q62 60 70 54" stroke="#F8F0DC" stroke-width="1.5" fill="none" opacity="0.4" stroke-linecap="round"/>
  <path d="M80 63 Q91 63 91 69 Q91 75 80 74" stroke="#7A8C6E" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M44 50 Q46 43 44 36" stroke="#7A8C6E" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" opacity="0.5"/>
  <path d="M55 52 Q57 45 55 38" stroke="#7A8C6E" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.35s" opacity="0.5"/>
</svg>'''

MOCHA_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="55" cy="84" rx="30" ry="5" fill="#C8954A" opacity="0.2"/>
  <path d="M26 58 L30 80 Q30 83 33 83 L77 83 Q80 83 80 80 L84 58 Z" fill="#2A1208" opacity="0.95"/>
  <rect x="26" y="53" width="58" height="7" rx="3" fill="#3D1A08" opacity="0.9"/>
  <ellipse cx="55" cy="53" rx="29" ry="6" fill="#4A2010" opacity="0.9"/>
  <ellipse cx="55" cy="51" rx="22" ry="5" fill="#F8F0DC" opacity="0.9"/>
  <path d="M40 50 Q48 44 55 48 Q62 52 70 46" stroke="#C8954A" stroke-width="1.5" fill="none" opacity="0.5" stroke-linecap="round"/>
  <path d="M80 60 Q91 60 91 66 Q91 72 80 71" stroke="#C8954A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M42 44 Q44 37 42 30" stroke="#EDD9B8" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" opacity="0.6"/>
  <path d="M55 46 Q57 39 55 32" stroke="#EDD9B8" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.35s" opacity="0.6"/>
  <path d="M68 44 Q70 37 68 30" stroke="#EDD9B8" stroke-width="1.8" fill="none" stroke-linecap="round" class="steam-path" style="animation-delay:.7s" opacity="0.6"/>
</svg>'''

CROISSANT_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M20 68 Q30 40 55 38 Q80 36 90 68 Q75 78 55 76 Q35 74 20 68 Z" fill="#C8954A" opacity="0.9"/>
  <path d="M22 65 Q32 45 55 42 Q78 39 88 65" fill="#E8C17A" opacity="0.7"/>
  <path d="M28 60 Q36 48 55 46 Q74 44 82 60" fill="#D4A44C" opacity="0.5"/>
  <path d="M20 68 Q28 62 35 56 Q42 50 55 48" stroke="#C8954A" stroke-width="1.5" fill="none" opacity="0.4"/>
  <path d="M90 68 Q82 62 75 56 Q68 50 55 48" stroke="#C8954A" stroke-width="1.5" fill="none" opacity="0.4"/>
  <ellipse cx="55" cy="76" rx="30" ry="5" fill="#1C0F0A" opacity="0.15"/>
</svg>'''

GRANOLA_SVG = '''<svg width="110" height="110" viewBox="0 0 110 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="55" cy="80" rx="34" ry="12" fill="#EDD9B8" opacity="0.9"/>
  <ellipse cx="55" cy="76" rx="30" ry="10" fill="#E8C17A" opacity="0.8"/>
  <circle cx="40" cy="74" r="5" fill="#C8954A" opacity="0.7"/>
  <circle cx="55" cy="72" r="6" fill="#D4A44C" opacity="0.8"/>
  <circle cx="68" cy="75" r="5" fill="#C8954A" opacity="0.7"/>
  <circle cx="47" cy="68" r="4" fill="#E8C17A"/>
  <circle cx="62" cy="69" r="4" fill="#D4A44C"/>
  <circle cx="44" cy="80" r="3" fill="#C8954A" opacity="0.6"/>
  <circle cx="66" cy="82" r="3" fill="#C8954A" opacity="0.6"/>
  <path d="M38 62 Q45 55 55 53 Q65 51 72 58" stroke="#7A8C6E" stroke-width="2" fill="none" stroke-linecap="round"/>
  <circle cx="42" cy="58" r="3" fill="#7A8C6E" opacity="0.7"/>
  <circle cx="68" cy="57" r="3" fill="#7A8C6E" opacity="0.7"/>
  <ellipse cx="55" cy="88" rx="28" ry="4" fill="#C8954A" opacity="0.15"/>
</svg>'''


CATEGORIES = [
    {'name': 'Espresso Classics', 'slug': 'espresso', 'description': 'The canon. Every great coffee tradition flows from these.', 'order': 1},
    {'name': 'Milk & Foam', 'slug': 'milk-foam', 'description': 'Where espresso meets craft steaming. Texture, temperature, and balance.', 'order': 2},
    {'name': 'Cold & Iced', 'slug': 'cold-iced', 'description': 'Patience brewed cold. Time is the ingredient.', 'order': 3},
    {'name': 'Specialty', 'slug': 'specialty', 'description': 'Beyond the bean. Ceremonial matcha, rich hot chocolate, and seasonal creations.', 'order': 4},
    {'name': 'Food', 'slug': 'food', 'description': 'Crafted to complement your cup, never compete with it.', 'order': 5},
]

MENU_ITEMS = [
    # Espresso Classics
    {
        'category': 'espresso', 'name': 'Single Origin Espresso', 'slug': 'single-origin-espresso',
        'tagline': 'Unadulterated. As the farmer intended.',
        'description': 'Thirty millilitres of precision. We pull single-origin beans at 9 bar, targeting a 25-second extraction that reveals the terroir of the farm it came from. This week: Ethiopia Yirgacheffe, with notes of bergamot and wild blueberry.',
        'price': '3.50', 'origin': 'Ethiopia, Yirgacheffe',
        'flavor_notes': 'Bergamot, Wild Blueberry, Dark Chocolate',
        'is_featured': True, 'is_loyalty_eligible': True, 'calories': 5, 'prep_time_minutes': 3,
        'illustration_svg': ESPRESSO_SVG,
    },
    {
        'category': 'espresso', 'name': 'Doppio', 'slug': 'doppio',
        'tagline': 'Double the intention.',
        'description': 'A double shot pulled from 18 grams of freshly ground single-origin coffee. Two ristrettos combined into a powerful, complex 60ml concentrate. The barista standard.',
        'price': '4.00', 'origin': 'Colombia, Huila',
        'flavor_notes': 'Dark Chocolate, Walnut, Brown Sugar',
        'is_featured': False, 'calories': 10, 'prep_time_minutes': 3,
        'illustration_svg': ESPRESSO_SVG,
    },
    {
        'category': 'espresso', 'name': 'Americano', 'slug': 'americano',
        'tagline': 'Espresso, extended.',
        'description': 'Hot water poured first, then a double espresso placed on top to preserve the crema. 150ml of clarity. A bridge between the intensity of espresso and the drinkability of filter.',
        'price': '3.80', 'price_medium': '4.30', 'origin': 'Honduras, Copan',
        'flavor_notes': 'Caramel, Hazelnut, Citrus Peel',
        'is_featured': False, 'calories': 10, 'prep_time_minutes': 4,
        'illustration_svg': ESPRESSO_SVG,
    },
    {
        'category': 'espresso', 'name': 'Macchiato', 'slug': 'macchiato',
        'tagline': 'Stained with purpose.',
        'description': 'A single or double espresso marked with a spoonful of dense milk foam. The Italian macchiato corrects for bitterness without diluting the shot. Small, potent, intentional.',
        'price': '3.70', 'origin': 'Kenya, Nyeri',
        'flavor_notes': 'Red Currant, Toffee, Cedar',
        'is_featured': False, 'calories': 25, 'prep_time_minutes': 4,
        'illustration_svg': ESPRESSO_SVG,
    },
    {
        'category': 'espresso', 'name': 'Lungo', 'slug': 'lungo',
        'tagline': 'The long pull.',
        'description': 'A 40-second extraction using the same grind as espresso, allowing 100ml to flow. Different compounds are extracted at this length, creating a less intense but more bitter, complex cup.',
        'price': '3.60', 'origin': 'Guatemala, Antigua',
        'flavor_notes': 'Dark Cocoa, Smoke, Brown Sugar',
        'is_featured': False, 'calories': 8, 'prep_time_minutes': 4,
        'illustration_svg': ESPRESSO_SVG,
    },
    # Milk & Foam
    {
        'category': 'milk-foam', 'name': 'Ritual Cappuccino', 'slug': 'ritual-cappuccino',
        'tagline': 'Equal thirds, infinite craft.',
        'description': 'Equal thirds espresso, steamed milk, and dense microfoam. We use whole milk textured to 65C and serve it at 150ml. The classic Italian morning drink, made with a focus on proportion and temperature.',
        'price': '4.20', 'price_medium': '4.80',
        'flavor_notes': 'Chocolate, Cream, Caramel',
        'origin': 'Blend, Ethiopia + Brazil',
        'is_featured': True, 'is_loyalty_eligible': True, 'calories': 110, 'prep_time_minutes': 5,
        'illustration_svg': CAPPUCCINO_SVG,
    },
    {
        'category': 'milk-foam', 'name': 'House Latte', 'slug': 'house-latte',
        'tagline': 'Precision milk. A single canvas.',
        'description': 'A double espresso with 200ml of velvety steamed whole milk. Our baristas pour free-hand latte art into every cup. The milk is textured to a fine, silky microfoam at exactly 65 degrees.',
        'price': '4.50', 'price_medium': '5.00', 'price_large': '5.50',
        'flavor_notes': 'Milk Chocolate, Vanilla, Hazelnut',
        'origin': 'Blend, Colombia + Kenya',
        'is_featured': True, 'is_loyalty_eligible': True, 'calories': 190, 'prep_time_minutes': 5,
        'illustration_svg': LATTE_SVG,
    },
    {
        'category': 'milk-foam', 'name': 'Flat White', 'slug': 'flat-white',
        'tagline': 'The antipodean way.',
        'description': 'A ristretto double shot with higher coffee-to-milk ratio than a latte. 160ml total, poured with dense, velvety microfoam straight from the jug. More coffee flavour, less milk.',
        'price': '4.40', 'origin': 'Blend, Australia Roast',
        'flavor_notes': 'Toffee, Dark Cocoa, Butter',
        'is_featured': True, 'is_loyalty_eligible': True, 'calories': 150, 'prep_time_minutes': 5,
        'illustration_svg': CAPPUCCINO_SVG,
    },
    {
        'category': 'milk-foam', 'name': 'Cortado', 'slug': 'cortado',
        'tagline': 'Cut. Balanced. Exact.',
        'description': 'Equal parts espresso and warm steamed milk in a small glass. No foam. The Spanish cortado cuts the espresso acidity without the ceremony of latte art. 90ml of focused balance.',
        'price': '4.10', 'origin': 'Blend, Colombia',
        'flavor_notes': 'Hazelnut, Caramel, Light Chocolate',
        'is_featured': False, 'calories': 70, 'prep_time_minutes': 5,
        'illustration_svg': CAPPUCCINO_SVG,
    },
    {
        'category': 'milk-foam', 'name': 'Mocha', 'slug': 'mocha',
        'tagline': 'Named after the ancient port.',
        'description': 'High-grade dark chocolate syrup combined with a double espresso, then topped with 200ml of steamed milk. Named after Mocha, Yemen, once the world\'s greatest coffee port. Rich and indulgent without excess.',
        'price': '4.80', 'price_medium': '5.40', 'price_large': '5.90',
        'flavor_notes': 'Dark Chocolate, Espresso, Cream',
        'origin': 'Blend, Yemen Tribute',
        'is_featured': False, 'calories': 260, 'prep_time_minutes': 6,
        'illustration_svg': MOCHA_SVG,
    },
    # Cold & Iced
    {
        'category': 'cold-iced', 'name': 'Signature Cold Brew', 'slug': 'signature-cold-brew',
        'tagline': '18 hours. No heat. No compromise.',
        'description': 'Coarsely ground single-origin beans steeped in filtered cold water for 18 hours. The result is extraordinarily smooth, low-acid, and naturally sweet. Served over hand-chipped ice.',
        'price': '4.80', 'price_large': '5.80',
        'origin': 'Ethiopia, Guji',
        'flavor_notes': 'Dark Cherry, Chocolate, Smooth',
        'is_featured': True, 'is_loyalty_eligible': True, 'calories': 15, 'prep_time_minutes': 2,
        'illustration_svg': COLD_BREW_SVG,
    },
    {
        'category': 'cold-iced', 'name': 'Nitro Cold Brew', 'slug': 'nitro-cold-brew',
        'tagline': 'Cascades like stout. Tastes like silk.',
        'description': 'Our 18-hour cold brew concentrate infused with nitrogen under pressure. It pours with a dramatic cascade and settles into a creamy, stout-like texture. Sweet, smooth, and served without ice.',
        'price': '5.50',
        'origin': 'Ethiopia, Guji',
        'flavor_notes': 'Cream, Dark Cherry, Cocoa',
        'is_featured': False, 'calories': 20, 'prep_time_minutes': 3,
        'illustration_svg': COLD_BREW_SVG,
    },
    {
        'category': 'cold-iced', 'name': 'Iced Pour Over', 'slug': 'iced-pour-over',
        'tagline': 'Flash-chilled. Every nuance preserved.',
        'description': 'A slow pour over brewed directly onto ice, flash-chilling the coffee to lock in volatile aromatics that would dissipate with heat. The cleanest, most complex iced coffee.',
        'price': '5.20',
        'origin': 'Japan, Kono Method',
        'flavor_notes': 'Jasmine, Peach, Honey',
        'is_featured': False, 'calories': 10, 'prep_time_minutes': 7,
        'illustration_svg': POUR_OVER_SVG,
    },
    {
        'category': 'cold-iced', 'name': 'Iced Oat Latte', 'slug': 'iced-oat-latte',
        'tagline': 'Cold, creamy, and botanical.',
        'description': 'A double espresso over ice with creamy barista oat milk. The oat milk\'s natural sweetness complements the espresso without overpowering. A crowd-favourite that we are proud of.',
        'price': '5.00', 'price_large': '5.80',
        'origin': 'Blend, Colombia',
        'flavor_notes': 'Oat, Caramel, Vanilla',
        'is_featured': False, 'is_loyalty_eligible': True, 'calories': 140, 'prep_time_minutes': 4,
        'illustration_svg': COLD_BREW_SVG,
    },
    # Specialty
    {
        'category': 'specialty', 'name': 'Ceremonial Matcha', 'slug': 'ceremonial-matcha',
        'tagline': 'Grade A. Whisked to order.',
        'description': 'Ceremonial-grade Uji matcha whisked with a bamboo chasen in a traditional ceramic bowl, then combined with steamed oat milk. Earthy, grassy, and gently sweet with no bitterness.',
        'price': '5.20', 'price_large': '5.90',
        'origin': 'Uji, Japan',
        'flavor_notes': 'Umami, Grass, Honey, Cream',
        'is_featured': True, 'is_loyalty_eligible': True, 'calories': 155, 'prep_time_minutes': 6,
        'illustration_svg': MATCHA_SVG,
    },
    {
        'category': 'specialty', 'name': 'Spiced Chai Latte', 'slug': 'spiced-chai-latte',
        'tagline': 'Whole spice. Hand-blended.',
        'description': 'Our house chai blend is made from whole cinnamon, green cardamom, cloves, ginger, and black pepper. Steeped in hot water and combined with steamed milk. Warming without being cloying.',
        'price': '4.80', 'price_large': '5.40',
        'origin': 'House Blend, India Inspired',
        'flavor_notes': 'Cinnamon, Cardamom, Ginger, Clove',
        'is_featured': False, 'is_loyalty_eligible': True, 'calories': 180, 'prep_time_minutes': 6,
        'illustration_svg': MATCHA_SVG,
    },
    {
        'category': 'specialty', 'name': 'Single Origin Hot Chocolate', 'slug': 'single-origin-hot-chocolate',
        'tagline': 'Bean-to-cup. Both kinds.',
        'description': 'Not cocoa powder. We use single-origin 70% Peruvian dark chocolate, finely chopped and melted into steamed whole milk. Thick, complex, and deeply satisfying.',
        'price': '4.90', 'price_large': '5.50',
        'origin': 'Peru, Piura',
        'flavor_notes': 'Dark Chocolate, Red Fruit, Vanilla',
        'is_featured': False, 'is_loyalty_eligible': False, 'calories': 280, 'prep_time_minutes': 6,
        'illustration_svg': MOCHA_SVG,
    },
    # Food
    {
        'category': 'food', 'name': 'Butter Croissant', 'slug': 'butter-croissant',
        'tagline': 'All butter. 72 layers.',
        'description': 'Made locally by our bakery partner using only French AOP butter, strong bread flour, and two days of laminating. Served warm from the oven. Pairs with any espresso drink.',
        'price': '3.20',
        'flavor_notes': 'Butter, Honey, Light',
        'is_featured': False, 'is_loyalty_eligible': False, 'calories': 310, 'prep_time_minutes': 2,
        'illustration_svg': CROISSANT_SVG,
    },
    {
        'category': 'food', 'name': 'Granola & Yogurt Bowl', 'slug': 'granola-yogurt-bowl',
        'tagline': 'Toasted in-house daily.',
        'description': 'Rolled oats toasted with local honey, almonds, pumpkin seeds, and a touch of cinnamon. Served over thick Greek yogurt with seasonal fruit compote. Substantial and uncluttered.',
        'price': '5.80',
        'flavor_notes': 'Honey, Almond, Oat, Berry',
        'is_featured': False, 'is_loyalty_eligible': False, 'calories': 380, 'prep_time_minutes': 3,
        'illustration_svg': GRANOLA_SVG,
    },
    {
        'category': 'food', 'name': 'Almond Cardamom Cake', 'slug': 'almond-cardamom-cake',
        'tagline': 'Baked with intention.',
        'description': 'A dense, moist almond flour cake spiced with freshly ground green cardamom. No gluten. Made fresh every morning. Designed to complement a cortado or flat white without competing.',
        'price': '4.50',
        'flavor_notes': 'Almond, Cardamom, Vanilla',
        'is_featured': False, 'is_loyalty_eligible': False, 'calories': 340, 'prep_time_minutes': 2,
        'illustration_svg': GRANOLA_SVG,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with Brew Ritual menu data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding menu categories...')
        cat_map = {}
        for c in CATEGORIES:
            obj, created = Category.objects.get_or_create(
                slug=c['slug'],
                defaults={
                    'name': c['name'],
                    'description': c.get('description', ''),
                    'order': c.get('order', 0),
                }
            )
            cat_map[c['slug']] = obj
            self.stdout.write(f"  {'Created' if created else 'Exists'}: {obj.name}")

        self.stdout.write('Seeding menu items...')
        for item in MENU_ITEMS:
            cat = cat_map.get(item['category'])
            if not cat:
                continue
            defaults = {
                'name': item['name'],
                'tagline': item.get('tagline', ''),
                'description': item['description'],
                'price': item['price'],
                'price_medium': item.get('price_medium'),
                'price_large': item.get('price_large'),
                'illustration_svg': item.get('illustration_svg', ''),
                'origin': item.get('origin', ''),
                'flavor_notes': item.get('flavor_notes', ''),
                'is_available': True,
                'is_featured': item.get('is_featured', False),
                'is_loyalty_eligible': item.get('is_loyalty_eligible', True),
                'calories': item.get('calories'),
                'prep_time_minutes': item.get('prep_time_minutes', 5),
            }
            obj, created = MenuItem.objects.get_or_create(
                slug=item['slug'],
                defaults={'category': cat, **defaults}
            )
            if not created:
                for k, v in defaults.items():
                    setattr(obj, k, v)
                obj.category = cat
                obj.save()
            self.stdout.write(f"  {'Created' if created else 'Updated'}: {obj.name}")

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@brewritual.com', 'admin123')
            self.stdout.write('Created superuser: admin / admin123')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(MENU_ITEMS)} items across {len(CATEGORIES)} categories.'
        ))

# Brew Ritual — Full-Stack Coffee Ordering Platform

A production-ready Django 5.1 web application for a specialty coffee shop.

## Quick Start

```bash
# 1. Install dependencies
pip install django==5.1 pillow crispy-bootstrap5 django-crispy-forms

# 2. Run migrations
python manage.py migrate

# 3. Seed menu & create admin
python manage.py seed_menu

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Run
python manage.py runserver
```

Visit http://127.0.0.1:8000

## Admin
- URL: /admin/
- Username: `admin`  Password: `admin123`

## Features
- Full menu with SVG illustrations (no real images needed)
- User auth: register, login, profile
- Cart & checkout (session-based for guests, user-based when logged in)
- Loyalty programme: 10 stamps = 1 free drink, 4 tiers (Bronze/Silver/Gold/Platinum)
- Ritual Guide: interactive brew methods with animated glass visualisations
- 67 passing tests

## Running Tests
```bash
python manage.py test tests --verbosity=2
```

## Stack
- Django 5.1 · SQLite (swap to PostgreSQL in production)
- Custom CSS design system (no Bootstrap)
- Vanilla JS (no framework)
- Fonts: Playfair Display, DM Sans, DM Mono (Google Fonts)

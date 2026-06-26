from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon_svg = models.TextField(blank=True, help_text="SVG markup for the category icon")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_medium = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_large = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    illustration_svg = models.TextField(blank=True, help_text="SVG illustration for this item")
    origin = models.CharField(max_length=100, blank=True)
    flavor_notes = models.CharField(max_length=200, blank=True, help_text="Comma-separated, e.g. Chocolate, Caramel, Hazelnut")
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_loyalty_eligible = models.BooleanField(default=True, help_text="Counts toward loyalty stamps")
    calories = models.PositiveIntegerField(null=True, blank=True)
    prep_time_minutes = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def get_price_for_size(self, size='S'):
        if size == 'M' and self.price_medium:
            return self.price_medium
        if size == 'L' and self.price_large:
            return self.price_large
        return self.price

    def has_sizes(self):
        return self.price_medium or self.price_large

    @property
    def flavor_list(self):
        if self.flavor_notes:
            return [f.strip() for f in self.flavor_notes.split(',')]
        return []

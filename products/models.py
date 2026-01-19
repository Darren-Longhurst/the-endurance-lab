from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    is_special_offer = models.BooleanField(default=False)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def has_variants(self):
        """
        Returns True if the product has at least one variant.
        Uses the 'related_name' from ProductVariant to check existence.
        """
        return self.variants.exists()

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant_type = models.CharField(max_length=254)
    price_modifier = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    variant_value = models.CharField(max_length=254)
    stock_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.variant_type}: {self.variant_value}"

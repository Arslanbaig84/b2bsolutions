from django.db import models
from base.models import BaseModel
from products.models import Product
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Review(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self) -> str:
        return f'{self.rating} for {self.product} by {self.user}'

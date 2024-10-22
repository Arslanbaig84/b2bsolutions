from django.db import models
from base.models import BaseModel
from users.models import CustomUser, Industry
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import datetime
from sorl.thumbnail import ImageField

# Create your models here.
class Product(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    industry = models.ManyToManyField(Industry, related_name='industry_products')
    product_name = models.CharField(max_length=100)
    product_model = models.CharField(max_length=100)
    manufacturing_year = models.PositiveIntegerField(validators=[
        MinValueValidator(1960),
        MaxValueValidator(datetime.date.today().year)
    ])
    hours_operation = models.PositiveIntegerField()
    product_location = models.CharField(max_length=200)
    product_description = models.TextField(max_length=500)
    product_price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    product_images = models.    ImageField(upload_to='products')
    
    def __str__(self) -> str:
        return self.product_name

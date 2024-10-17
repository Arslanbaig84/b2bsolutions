from django.db import models
import uuid

# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
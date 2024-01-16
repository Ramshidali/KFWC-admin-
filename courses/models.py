import uuid

from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal
from versatileimagefield.fields import VersatileImageField

from main.models import BaseModel

STATUS = (
    ('010', 'Enable'),
    ('015', 'Disable'),
)

# Create your models here.
class Course(BaseModel):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=3, choices=STATUS)
    image = VersatileImageField('Image', upload_to="courses/course", blank=True, null=True)
    mrp = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'courses'
        verbose_name = ('Courses')
        verbose_name_plural = ('Courses')
        
    def __str__(self):
        return str(self.id)

class Details(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'units'
        verbose_name = ('Unit')
        verbose_name_plural = ('Unit')
        
    def __str__(self):
        return str(self.id)
from django.db import models

# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    image = models.ImageField(upload_to='photos/')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='photos')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Photo {self.id}"

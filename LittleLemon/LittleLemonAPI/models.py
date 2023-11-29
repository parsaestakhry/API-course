from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, db_constraint=False, default=1
    )
    
    inventory = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

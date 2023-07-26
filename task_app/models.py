from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=5000,unique = True)
    
    def __str__(self):
        return self.category
    
class Product(models.Model):
    name = models.CharField(max_length=1000000, unique=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, unique=False)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return self.title


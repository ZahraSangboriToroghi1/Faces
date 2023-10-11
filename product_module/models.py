from django.db import models


# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان محصول')
    description = models.TextField(verbose_name='توضیحات محصول')
    price = models.IntegerField(verbose_name='قیمت محصول')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

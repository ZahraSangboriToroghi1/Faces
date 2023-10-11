from django.db import models


# Create your models here.

class FaceRecognition(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    image = models.ImageField(upload_to='images/', verbose_name='تصویر')

    def __str__(self):
        return str(self.create_date)

    class Meta:
        verbose_name = 'مدل تشخیص چهره'
        verbose_name_plural = 'مدل های تشخیص چهره'

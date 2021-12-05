from django.db import models


# Create your models here.

# модель Міста
class City(models.Model):
    city_name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Cities"

    # стрічкове представлення міста
    def __str__(self):
        return self.city_name

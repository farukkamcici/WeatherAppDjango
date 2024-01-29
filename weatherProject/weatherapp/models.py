from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission




# Create your models here.
class CustomUser(AbstractUser):
    my_city=models.CharField(max_length=25, null=True)

    def save(self, *args, **kwargs):
        # Your custom logic here
        if self.my_city:
            self.my_city = self.my_city.title()
        super().save(*args, **kwargs)



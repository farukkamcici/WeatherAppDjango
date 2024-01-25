from django.db import models

# Create your models here.
class City (models.Model):
    name= models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        app_label= "weatherapp"
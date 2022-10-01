from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User,
                        default = 1,
                        null = True, 
                        on_delete = models.SET_NULL
                        )
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to ='pics')

  
    def __str__(self):
        return self.title
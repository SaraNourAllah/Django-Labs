from django.db import models

class Courses (models.Model):
    name = models.CharField(max_length=50 )
    image = models.ImageField (upload_to='courses/images/' , null = True )

    def __str__(self):
        return self.name
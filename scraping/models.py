from django.db import models

class CategoryModel(models.Model):
    category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.category
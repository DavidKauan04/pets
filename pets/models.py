from django.db import models

# Create your models here.
class GenderPets(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    DEFAULT = 'Not informed'


class Pet(models.Model):
    name = models.CharField(max_length = 50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length = 20, choices=GenderPets.choices, default=GenderPets.DEFAULT)

    groups = models.ForeignKey(
        'groups.Group',
        related_name='groups',
        null=True,
        on_delete=models.CASCADE
    )



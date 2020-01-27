from django.db import models

from . import views

# Create your models here.
# users = tier + matches + ...


class users(models.Model):
    area = models.CharField(max_length=3)
    userNumber = models.IntegerField()
    summonerName = models.CharField(max_length=20)
    user_create_date = models.DateTimeField('date published')

    def __str__(self):
        return self.summonerName


class matches(models.Model):
    matches = models.ForeignKey('users', on_delete=models.CASCADE)
    order_matches = models.IntegerField()
    # match_date = models.DateTimeField(default="N/A")
    match_wl = models.CharField(max_length=4, default="N/A")





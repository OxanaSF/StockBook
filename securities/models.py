from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol

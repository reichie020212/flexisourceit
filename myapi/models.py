from django.db import models
from model_utils.models import TimeStampedModel


class Stock(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        verbose_name='Name',
        unique=True,
    )
    price = models.DecimalField(
        'price',
        decimal_places=2,
        max_digits=20,
    )


class Account(TimeStampedModel):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name='First Name',
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='Last Name',
    )

    def get_stocks(self):
        return self.mystock_set.all()


class MyStock(TimeStampedModel):
    account = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
    )
    stock = models.ForeignKey(
        'Stock',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (
            ('account', 'stock',),
        )

    def get_total_invested(self):
        return self.stock.price * self.quantity

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from utils.general_model import GeneralModel
from shop.models import Product

User = get_user_model()


# Create your models here.
class Review(GeneralModel):
    STATUS_CHOICES = (
        ('A', "Accepted"),
        ('W', "Awaiting confirmation"),
        ('F', "Failed"),
    )
    product = models.ForeignKey(Product, related_name="reviews",
                                on_delete=models.CASCADE,
                                verbose_name=_("Product"),)
    user = models.ForeignKey(User, related_name="reviews",
                             on_delete=models.CASCADE,
                             verbose_name=_("User"),)
    comment = models.TextField(verbose_name=_("comment"),)
    rate = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Rate"),)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
                              default='W', verbose_name=_("Status"))

    def __str__(self):
        if len(self.comment) >= 100:
            return self.user.full_name + ': ' + self.comment[:100]
        return self.user.full_name + ': ' + self.comment

    def get_full_name(self):
        return self.user.full_name
    get_full_name.short_description = _("full name")

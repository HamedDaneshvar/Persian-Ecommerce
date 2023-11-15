from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel


class Category(GeneralModel):
    name = models.CharField(
        max_length=250,
        verbose_name=_("Name"),)
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name=_("Slug"),)

    class Meta:
        ordering = ["name",]
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug,])


class Product(GeneralModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Category"))
    name = models.CharField(
        max_length=250,
        verbose_name=_("Name"),)
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name=_("Slug"),)
    image = models.ImageField(
        upload_to="products/%Y/%m/%d",
        blank=True,
        verbose_name=_("Image"),)
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Price"),)
    available = models.BooleanField(
        default=True,
        verbose_name=_("Available"),)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug",]),
            models.Index(fields=["name",]),
            models.Index(fields=["-create_at",]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug,])

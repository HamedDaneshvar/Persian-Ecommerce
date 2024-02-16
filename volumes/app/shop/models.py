from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel


class Category(GeneralModel):
    """
    Model representing a category for products.
    """

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
        """
        String representation of the category.
        """

        return self.name

    def get_absolute_url(self):
        """
        Get the absolute URL of the category.
        """

        return reverse('shop:product_list_by_category', args=[self.slug,])


class Product(GeneralModel):
    """
    Model representing a product in the shop.
    """

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
        null=True,
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
    users_wishlist = models.ManyToManyField(
        get_user_model(),
        related_name="user_wishlist",
        blank=True,)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug",]),
            models.Index(fields=["name",]),
            models.Index(fields=["-create_at",]),
        ]

    def __str__(self):
        """
        String representation of the product.
        """

        return self.name

    def get_absolute_url(self):
        """
        Get the absolute URL of the product.
        """

        return reverse('shop:product_detail', args=[self.id, self.slug,])


class Product_Image(GeneralModel):
    image = models.ImageField(
        upload_to="products/%Y/%m/%d",
        verbose_name=_("Image"),)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Product"))

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return self.product.name + " Image"

    def get_product_name(self):
        return self.product.name
    get_product_name.short_description = _("Product Name")

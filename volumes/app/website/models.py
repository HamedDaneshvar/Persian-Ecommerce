from django.db import models
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel


class Slider(GeneralModel):
    image = models.ImageField(verbose_name=_("Image"))
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    subtitle = models.CharField(max_length=250, blank=True, null=True,
                                verbose_name=_("Subtitle"))
    link = models.URLField(blank=True, null=True, verbose_name=_("Link"))
    status = models.BooleanField(default=False, verbose_name=_('Display'))

    class Meta:
        verbose_name = _("Slider")
        verbose_name_plural = _("Sliders")

    def __str__(self):
        if len(self.title) > 100:
            return self.title[:100]
        return self.title

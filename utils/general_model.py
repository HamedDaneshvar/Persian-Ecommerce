from django.db import models
from django.utils.translation import gettext as _


class GeneralModel(models.Model):
	create_at = models.DateTimeField(
		auto_now_add=True
		verbose_name=_('Created Time'),)
	updated_at = models.DateTimeField(
		auto_now=True
		verbose_name=_('Updated Time'),)

	class Meta:
		abstract = True

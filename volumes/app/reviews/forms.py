from django import forms
from django.utils.translation import gettext as _
from reviews.models import Review


class ReviewForm(forms.ModelForm):
    RATE_CHOICES = (
        (1, '1 star'),
        (2, '2 star'),
        (3, '3 star'),
        (4, '4 star'),
        (5, '5 star'),
    )
    rate = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=RATE_CHOICES,)

    class Meta:
        model = Review
        fields = ("comment", "rate",)
        widgets = {
            'comment': forms.Textarea(attrs={"rows": 30, "cols": 10,
                                             "data-max-length": 200,
                                             "class": "form-control mb-3",
                                             "placeholder":
                                             _("نظرخود را بنویسید ...")}),
        }

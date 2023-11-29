from django import forms


class CouponApplyForm(forms.Form):
    """
    Form for applying a coupon code.

    This form allows users to enter a coupon code to apply it for discounts or
    special offers.

    Fields:
        code (CharField): The field for entering the coupon code.

    Example:
        To apply a coupon code, instantiate an instance of this form and
        render it in a template. Upon submission, the code entered in the form
        can be processed to apply the corresponding coupon benefits.

    """
    code = forms.CharField()

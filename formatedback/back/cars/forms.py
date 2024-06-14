from django import forms


class CarSearchForm(forms.Form):
    brand_country = forms.CharField(required=False)


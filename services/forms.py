from django import forms
from .models import Hall, HallRent, HallImage

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = [
            "name", "description", "location", "capacity", 'batch',
            "area_size", "parking_capacity", "year_built",
            "is_government_property",
        ]


class HallRentForm(forms.ModelForm):
    class Meta:
        model = HallRent
        fields = ["season", "shift", "price"]
        widgets = {
            "season": forms.Select(attrs={'class':'form-select'}),
            "shift": forms.Select(attrs={'class':'form-select'}),
            "price": forms.NumberInput(attrs={'class':'form-control'})
        }


class HallImageForm(forms.ModelForm):
    class Meta:
        model = HallImage
        fields = ["image", "caption"]

from django.forms import modelformset_factory
from .models import HallRent

HallRentFormSet = modelformset_factory(
    HallRent,
    form=HallRentForm,
    extra=0,
    can_delete=True
)


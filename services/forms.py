from django import forms
from .models import Hall, HallRent, HallImage
from django.forms import modelformset_factory
from .models import HallRent

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

HallRentFormSet = modelformset_factory(
    HallRent,
    form=HallRentForm,
    extra=0,
    can_delete=True
)


class HallImageForm(forms.ModelForm):
    class Meta:
        model = HallImage
        fields = ["image", "caption"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={'class': 'form-control'}),
            "caption": forms.TextInput(attrs={'class': 'form-control'}),
        }


HallImagesFormSet = modelformset_factory(
    HallImage,
    form=HallImageForm,
    extra=0,
    can_delete=True
)




from django import forms
from .models import Center, Hall, HallImage, Amenity
from django.forms import modelformset_factory
from .bangladesh_locations import BANGLADESH_DISTRICTS, BANGLADESH_CITIES

class CenterForm(forms.ModelForm):
    city = forms.ChoiceField(
        choices=[("", "Select City")] + BANGLADESH_CITIES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    district = forms.ChoiceField(
        choices=[("", "Select District")] + BANGLADESH_DISTRICTS,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Center
        fields = [
            "owner_user",
            "name",
            "description",
            "address",
            "latitude",
            "longitude",
            "city",
            "district",
            "country",
            "status",
            "contact_phone",
            "amenities",
        ]
        widgets = {
            "owner_user": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "address": forms.Textarea(attrs={"rows": 1, "class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "contact_phone": forms.TextInput(attrs={"class": "form-control"}),
            "latitude": forms.NumberInput(attrs={"class": "form-control"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "amenities": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        }
        labels = {
            "owner_user": "Center Owner",
        }

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = [
            "name",
            "capacity",
            "batch",
            "size",
            "price_currency",
            "price_per_hour",
            "price_per_day",
            "min_booking_hours",
            "latitude",
            "longitude",
            "description",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "batch": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "size": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "price_currency": forms.TextInput(attrs={"class": "form-control"}),
            "price_per_hour": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "price_per_day": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "min_booking_hours": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "latitude": forms.NumberInput(attrs={"class": "form-control", "step": "any"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control", "step": "any"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

HallFormSet = modelformset_factory(
    Hall,
    form=HallForm,
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

class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ["name", "icon"]
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter amenity name'}),
            "icon": forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




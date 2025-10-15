from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CUser, WebsiteConfiguration, SliderImage
from django.forms import modelformset_factory


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,  # optional on signup
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"})
    )


    class Meta:
        model = CUser
        fields = ("username", "first_name", "last_name", "email", "phone", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username", "autofocus": True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to built-in password fields
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        phone = self.cleaned_data.get("phone")
        if phone:
            user.phone = phone
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class WebsiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = WebsiteConfiguration
        fields = ["site_name", "logo", "about_us"]
        widgets = {
            "site_name": forms.TextInput(attrs={"class": "form-control"}),
            "about_us": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


class SliderImageForm(forms.ModelForm):
    class Meta:
        model = SliderImage
        fields = ["image", "caption", "caption_sub", "is_active"]
        widgets = {
            "caption": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter caption"}),
            "caption_sub": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter sub caption"}),
        }

SliderFormSet = modelformset_factory(
    SliderImage,
    form=SliderImageForm,
    extra=0,
    can_delete=True
)

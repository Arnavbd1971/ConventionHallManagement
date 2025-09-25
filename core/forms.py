from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CUser  # your custom user model

class CustomUserCreationForm(UserCreationForm):
    type = forms.ChoiceField(
        choices=[("member", "Member"), ("organizer", "Organizer"), ("admin", "Admin")],
        required=True,
    )

    class Meta:
        model = CUser
        fields = ("username", "email", "password1", "password2", "type")

    def save(self, commit=True):
        user = super().save(commit=False)   # don’t commit yet
        user.type = self.cleaned_data["type"]
        if commit:
            user.save()
        return user

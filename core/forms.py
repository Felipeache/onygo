from django import forms
from django.db import models
from django.forms import ModelForm
from datetime import datetime
from .models import Event, UserProfile, Message
from .services import validate_address
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm


def debug(*args):
    print("*********" * 10)
    print("*********" * 10)
    print("*********" * 10)
    print("*********" * 10)
    print("*********" * 10)
    print(args)
    print("*********" * 10)
    print("*********" * 10)
    print("*********" * 10)
    print("*********" * 10)
    print("*********" * 10)


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.DateInput):
    input_type = "time"


# Creating the message form
class Send_Message_Form(ModelForm):

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 20,
                "style": "resize: none",
                "placeholder": "Ecris ton message...",
            }
        )
    )

    class Meta:
        model = Message
        fields = ["text"]


# Creating the create event form
class Create_Event_Form(ModelForm):

    event_name = forms.CharField(
        min_length=8,
        max_length=45,
        widget=forms.Textarea(
            attrs={
                "rows": 1,
                "cols": 1,
                "style": "resize: none",
                "placeholder": "Title de ton événement...",
                "help_text": "Au moins 8 lettres",
            }
        ),
    )

    nber_of_places = forms.IntegerField(
        min_value=1, max_value=11, widget=forms.NumberInput(attrs={"value": 5})
    )

    city = forms.CharField(
        min_length=3,
        max_length=25,
        widget=forms.Textarea(
            attrs={
                "rows": 1,
                "cols": 1,
                "style": "resize: none",
                "placeholder": "Ville...",
                "help_text": "Ville de ton événement",
            }
        ),
    )

    event_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 20,
                "style": "resize: none",
                "placeholder": "Décris ton événement...",
            }
        )
    )

    class Meta:
        model = Event
        fields = [
            "event_name",
            "event_description",
            "nber_of_places",
            "event_address",
            "city",
            "date",
            "time",
        ]
        widgets = {
            "date": DateInput(attrs={"value": datetime.now().date()}),
            "time": forms.TimeInput(
                format="%HH:%MM", attrs={"type": "time", "value": "19:00", "step": 300}
            ),
        }

    # validating that the entered date is not before today
    def clean_date(self):
        today = datetime.now().date()  # tipo datetime
        date = self.cleaned_data["date"]  # tipo date
        if date < today:
            raise forms.ValidationError(
                "Nous ne pouvons crér un événement dans le passé!"
            )
        return date

    def clean_time(self):
        current_time = datetime.now().time()
        time = self.cleaned_data["time"]
        if time < current_time and self.cleaned_data["date"] <= datetime.now().date():
            raise forms.ValidationError(
                "Nous ne pouvons crér un événement dans le passé!"
            )
        return time

    def clean_event_address(self):

        if not validate_address(self.cleaned_data["event_address"], self.data["city"]):
            raise forms.ValidationError("Verifie l'addresse et la ville de ton événement")
        return self.cleaned_data["event_address"]


# Creating the Custom user creation form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        # help_texts = {
        #    'username': None,
        #    'email': None,
        #    'first_name': None,
        #    'last_name': None,
        #    'password1': None,
        #    'password2': None,
        # }


def save(self, commit=True):
    user = super(CustomUserCreationForm, self).save(commit=False)
    user.first_name = self.cleaned_data["username"]
    user.first_name = self.cleaned_data["first_name"]
    user.last_name = self.cleaned_data["last_name"]
    user.email = self.cleaned_data["email"]
    if commit:
        user.save()
    return user


class UserProfile_Form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["user_description", "city", "avatar"]


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        exclude = ["password"]


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        help_texts = {
            "password1": "Ton password",
            "password2": "Ton password encore une fois",
        }

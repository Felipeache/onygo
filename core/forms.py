from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from datetime import datetime
from .models import Event, UserProfile, Message
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.DateInput):
    input_type = 'time'

class Send_Message_Form(ModelForm):

    text =  forms.CharField ( widget = forms.Textarea (
                        attrs={
                                "rows":5,
                                "cols":20,
                                "style": "resize: none"
                                }
                        )
                    )

    class Meta:
        model = Message
        fields = ['text']

class Create_Event_Form(ModelForm):
    event_name = forms.CharField(min_length=4, max_length=25)

    nber_of_places = forms.IntegerField(min_value=1, max_value=11, widget=forms.NumberInput( attrs={'value':5}))

    zip_code = forms.IntegerField(min_value=11111, max_value=99999)

    event_description =  forms.CharField (
        widget = forms.Textarea (
                        attrs={
                                "rows":5,
                                "cols":20,
                                "style": "resize: none"
                                }
                        )
                    )


    class Meta:
        model = Event
        fields = [
                'event_name',
                'event_description',
                'nber_of_places',
                'event_address',
                'zip_code',
                'city',
                'date',
                'time',
                ]
        widgets = {
            'date': DateInput(attrs={'value':datetime.now().date()}),
            'time': forms.TimeInput(
                                format='%HH:%MM',
                                attrs={
                                            'type': 'time',
                                            'value': '19:00',
                                            'step': 300
                                        }
                                    )
                }

    def clean_date(self):
        today = datetime.now().date()  # tipo datetime
        date = self.cleaned_data['date']  # tipo date
        if date < today:
            raise forms.ValidationError(
                        "Nous ne pouvons crér un événement dans le passé!"
                    )
        return date

    def clean_time(self):
        crt_time = datetime.now().time()
        time = self.cleaned_data['time']
        if time < crt_time and self.cleaned_data['date'] <= datetime.now().date():
            raise forms.ValidationError(
                    "Nous ne pouvons crér un événement dans le passé!"
                )
        return time


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2'
                ]

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfile_Form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_description', 'address', 'city', 'avatar']


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        exclude = ['password']


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User

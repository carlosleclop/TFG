from django import forms
from transitweb.models import *
from django.utils.timezone import now
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class OccultationForm(forms.ModelForm):
    datePrediction = forms.DateField(help_text="Date of prediction",
                                     input_formats=('%d/%m/%Y','%d-%m-%Y'))
    timePrediction = forms.TimeField(help_text="Time of prediction")
    #location = forms.ForeignKey(Location)
    additionalInfo = forms.CharField(max_length=128, help_text="Extra info", required=False)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    #usersGo = forms.ManyToManyField(UserObserver)
    #location = forms.ForeignKey(Location)
    adenda = forms.CharField(widget=TinyMCE(attrs={'cols':80, 'rows':30}))

    class Meta:
        model = Occultation
        fields = ("datePrediction", "timePrediction", "additionalInfo", "adenda")

class TelescopeForm(forms.ModelForm):
    latitude = forms.DecimalField(max_digits=13, decimal_places=10, help_text="Latitude")
    longitude = forms.DecimalField(max_digits=13, decimal_places=10, help_text="Longitude")
    country = forms.CharField(max_length=128, help_text="Country")

    mobile = forms.BooleanField(help_text="Is a mobile telescope?", required=False)
    additionalInfo = forms.CharField(max_length=128, help_text="Additional info", required=False)

    class Meta:
        model = Telescope
        fields = ("latitude", "longitude",
                  "country", "mobile", "additionalInfo")

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

class UserProfileForm(forms.ModelForm):
    #website = forms.URLField(label="Website", required=False)
    public = forms.BooleanField(label="Public profile account?", required=False)

    class Meta:
        model = Profile
        fields = ("birth_date", "country", "website", "phone", "public")

class EditProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    birth_date = forms.DateField(required=False)
    country = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    public = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ("website", "birth_date", "country", "phone", "public")

class EditTelescopeForm(forms.ModelForm):
    mobile = forms.BooleanField(required=False)
    country = forms.CharField(required=False)
    latitude = forms.DecimalField(required=False)
    longitude = forms.DecimalField(required=False)
    additionalInfo = forms.CharField(required=False)

    class Meta:
        model = Telescope
        fields = ("mobile", "country", "latitude", "longitude", "additionalInfo")

"""
class ChangeAccount(forms.ModelForm):
    username = forms.CharField(default)
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")
"""

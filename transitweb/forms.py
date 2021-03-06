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
    attachedImage = forms.FileField(required = False)
    attachedFile = forms.ImageField(required = False)
    class Meta:
        model = Occultation
        fields = ("datePrediction", "timePrediction", "additionalInfo", "adenda", "attachedImage", "attachedFile")

class EquipmentForm(forms.ModelForm):
    latitude = forms.DecimalField(
            max_digits=22,
            decimal_places=18,
            help_text="Latitude (from the map)",
            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    longitude = forms.DecimalField(
            max_digits=22,
            decimal_places=18,
            help_text="Longitude (from the map)",
            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    country = forms.CharField(
            max_length=128,
            help_text="Country",
            widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.BooleanField(
            help_text="Is a mobile equipment? (select for mobile, no select for static)",
            required=False)
    additionalInfo = forms.CharField(
            max_length=128,
            help_text="Additional info",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Equipment
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

class EditEquipmentForm(forms.ModelForm):
    mobile = forms.BooleanField(required=False)
    country = forms.CharField(required=False)
    latitude = forms.DecimalField(required=False)
    longitude = forms.DecimalField(required=False)
    additionalInfo = forms.CharField(required=False)

    class Meta:
        model = Equipment
        fields = ("mobile", "country", "latitude", "longitude", "additionalInfo")

class AddResultForm(forms.ModelForm):
    report = forms.CharField(help_text="Data report", widget=forms.Textarea(attrs={'cols': 40, 'rows': 20}))
    adenda = forms.CharField(help_text="Other related information", required=False, widget=TinyMCE(attrs={'cols':40, 'rows':20}))
    #telescope = forms.ChoiceField(choices=((1, "opcion 1"), (2, "opcion 2")))

    class Meta:
        model = Result
        fields = ("report", "adenda")

"""
class ChangeAccount(forms.ModelForm):
    username = forms.CharField(default)
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")
"""

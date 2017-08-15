from django.db import models
from datetime import date, time
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce import models as tinymce_models

from django.template.defaultfilters import slugify

class Location(models.Model):
    latitude = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    longitude = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    attitude = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    country = models.CharField(max_length=128)
    additionalInfo = models.CharField(max_length=128)

    def __unicode__(self):
        return unicode(unicode(self.latitude) + "," + unicode(self.longitude))

class Telescope(models.Model):
    mobile = models.BooleanField(default=False)
    country = models.CharField(max_length=128, null=True)
    latitude = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    longitude = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    additionalInfo = models.CharField(max_length=128, null=True)
    # UserObserver isn't defined yet, "UserObserver" can be used in the same way
    user = models.ForeignKey("UserObserver", null=True)

    def __unicode__(self):
        return str(self.latitude) + " " + str(self.longitude)

class Profile(models.Model):
    """ en user: username, first_name, last_name, email, password """
    user = models.OneToOneField(User)

    birth_date = models.DateField(default=now, null=True)
    public = models.BooleanField(default=True)
    website = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    location = models.ForeignKey(Location, null=True)

    def __unicode__(self):
        return str(user.username)

class UserObserver(models.Model):
    user = models.OneToOneField(User)

    def get_UserObserver_with_telescope(find_telescope):
        for u in UserObserver.objects.all():
            if u.telescope == find_telescope:
                return u
        return None

    def __unicode__(self):
        return self.user.username

class UserAstronomer(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

class Occultation(models.Model):
    id = models.IntegerField(primary_key=True)
    datePrediction = models.DateField(default=now)
    timePrediction = models.TimeField(default=now)
    additionalInfo = models.CharField(max_length=128, null=True)
    usersGo = models.ManyToManyField(UserObserver, null=True)
    #slug = models.SlugField(unique=True)
    adenda = tinymce_models.HTMLField(null=True)

    def save(self, *args, **kwargs):
        id = Occultation.objects.all().count()
        #self.slug = slugify(str(self.id))
        super(Occultation, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode("Occultation " + unicode(self.additionalInfo))

class Subscription(models.Model):
    occultation = models.ForeignKey(Occultation)
    telescope = models.ForeignKey(Telescope)

    additionalInfo = models.CharField(max_length=4096, null=True)

    def __unicode__(self):
        return "no str info"
        return "Occultation: " + str(occultation) + ", user: " + str(telescope)

class Result(models.Model):
    telescope = models.ForeignKey(Telescope)
    occultation = models.ForeignKey(Occultation)

    report = models.CharField(max_length=65535)
    adenda = tinymce_models.HTMLField(null=True)

    def __unicode__(self):
        return str("Result ID: " + str(self.id))

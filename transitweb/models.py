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

class Equipment(models.Model):
    mobile = models.BooleanField(default=False)
    country = models.CharField(max_length=128, null=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=18, default=0)
    longitude = models.DecimalField(
            max_digits=22,
            decimal_places=18,
            default=0)
    additionalInfo = models.CharField(max_length=65535, null=True)
    # UserObserver isn't defined yet, "UserObserver" can be used instead
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

    def get_UserObserver_with_equipment(find_equipment):
        for u in UserObserver.objects.all():
            if u.equipment == find_equipment:
                return u
        return None

    def __unicode__(self):
        return self.user.username

class UserAstronomer(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

class Occultation(models.Model):
    datePrediction = models.DateField(default=now)
    timePrediction = models.TimeField(default=now)
    additionalInfo = models.CharField(max_length=128, null=True)
    usersGo = models.ManyToManyField(UserObserver, null=True)
    adenda = tinymce_models.HTMLField(null=True)
    reporter = models.ForeignKey(UserAstronomer, null=True)

    attachedFile = models.FileField(null = True)
    attachedImage = models.ImageField(null = True)

    def __unicode__(self):
        return unicode("Occultation " + unicode(self.additionalInfo))

class Subscription(models.Model):
    occultation = models.ForeignKey(Occultation)
    equipment = models.ForeignKey(Equipment)

    additionalInfo = models.CharField(max_length=4096, null=True)

    def __unicode__(self):
        return "no str info"
        return "Occultation: " + str(occultation) + ", user: " + str(equipment)

class Result(models.Model):
    equipment = models.ForeignKey(Equipment)
    occultation = models.ForeignKey(Occultation)

    report = models.CharField(max_length=65535)
    adenda = tinymce_models.HTMLField(null=True)

    def __unicode__(self):
        return str("Result ID: " + str(self.id))

class NotificationManager(models.Manager):
    NEW_OCCULT_MESSAGE = {
        "subject": "New occultation added",
        "message": "A new occultation has been added to the system. <br><br>Please, have a look at it and do not hesitate to ask any question to the reporter. <br><br>Regards."
    }

    NEW_RESULT_MESSAGE = {
        "subject": "New result of an occultation added",
        "message": "An user has uploaded a new result to the system. <br><br>Please, consider having a look at it, just for check the format. <br><br>Regards."
    }

    def send_notification_to_observers(
            self,
            message = NEW_OCCULT_MESSAGE,
            link = None):
        for user in UserObserver.objects.all():
            body = str(message.get("message"))
            if link is not None:
                body += "<br><br>Related link: <a href=\""
                body += str(link)
                body += "\">"
                body += str(link) + "</a>"
            self.create(
                    receiver = user.user,
                    subject = message.get("subject"),
                    message = body,
                    read = False)

    def send_notification_to_astronomers(self):
        pass

    def send_notification_to_everyone(self):
        pass

    def send_notification_to_someone(self, user):
        pass

class Notification(models.Model):
    receiver = models.ForeignKey(User)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=65535, null=True)
    read = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now=True)

    objects = NotificationManager()

    def __unicode__(self):
        return str(str(self.receiver) + ": " + str(self.subject))

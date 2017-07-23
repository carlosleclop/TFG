import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transitweb_project.settings")

import django
django.setup()

from django.db import models
from transitweb.models import *
from datetime import datetime, date, time
from django.contrib.auth.models import User

def populate():
    loc1 = add_location(37.196943, -3.6225, "piso")
    loc2 = add_location(36.526082, 37.9463712, "manbij")
    loc3 = add_location(53.44512, -6.485218, "otro")
    
    add_occult (location=loc1, dat=date(2017, 6, 7), tim=time(20,7))
    add_occult (location=loc2, dat=date(2018, 5, 1), tim=time(10,5))
    
    user = User.objects.create_user("user5", password="finisterre")
    user.is_superuser = False
    user.is_staff = True
    user.save()
    
    userob = UserObserver.objects.get_or_create(user=user, location=loc3)[0]
    userob.save()
    
    for l in Location.objects.all():
        for o in Occultation.objects.filter(location=l):
            print "- {0} - {1}".format(str(l), str(o))


def add_location(latitude, longitude, aditionalInfo):
    l = Location.objects.get_or_create(latitude=latitude, longitude=longitude)[0]
    l.aditionalInfo = aditionalInfo
    l.save()
    return l

def add_occult(location, dat, tim):
    o = Occultation.objects.get_or_create(location=location, datePrediction=dat)[0]
    o.save()
    return o

if __name__ == "__main__":
    print "Starting populate script"
    populate()

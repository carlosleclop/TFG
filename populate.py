import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transitweb_project.settings")

import django
django.setup()

from django.db import models
from transitweb.models import *
from datetime import datetime, date, time, timedelta
from django.contrib.auth.models import User
from random import randint, choice

def my_add_user(name):
    email = name+"@falsemail.com"
    user = User.objects.create_user(name, email=email, password="finisterre")

    profile = Profile()
    profile.birth_date = date(1991, 2, 24)
    profile.public = choice([True, False])
    profile.website = ""
    profile.phone = randint(600000000, 699999999)
    profile.user = user
    profile.save()
    
    return user

def my_add_observer(name):
    user = my_add_user(name)

    observer = UserObserver()
    observer.user = user
    observer.save()
    print "New Observer: " + name
    
    return observer
   
def my_add_astronomer(name):
    user = my_add_user(name)
    
    astronomer = UserAstronomer()
    astronomer.user = user
    astronomer.save()
    print "New Astronomer: " + name
    
    return astronomer

def my_add_occultation(astronomer_creator, future=True):
    if future:
        new_date = date.today() + timedelta(days=randint(0,1000))
    else:
        new_date = date.today() - timedelta(days=randint(1,1000))
    
    occult = Occultation()
    occult.datePrediction = new_date
    occult.timePrediction = time(randint(0, 23), randint(0, 59))
    occult.reporter = astronomer_creator
    occult.save()
    print "New occultation added"
    
    return occult

def my_add_equipment(observer_owner):
    equipment = Equipment()
    equipment.mobile = choice([True, False])
    equipment.user = observer_owner
    equipment.save()
    print "New equipment"
    
    return equipment

""" Subscription class is not being used anymore!
def my_add_subscription(occultation, equipment):
    subscription = Subscription()
    subscription.occultation = occultation
    subscription.equipment = equipment
    subscription.save()
    print "New subscription"
    
    return subscription
"""
def my_add_subscription(occultation, userObserver):
    occultation.usersGo.add(userObserver)
    occultation.save()

def my_add_result(occultation, equipment):
    result = Result()
    result.occultation = occultation
    result.equipment = equipment
    result.report = "This is a standard report with no real information"
    result.adenda = ""
    result.save()
    print "New result"

def populate():
    superastronomer = my_add_astronomer("carlos")
    superastronomer.user.is_staff = True
    superastronomer.user.is_superuser = True
    
    observer1 = my_add_observer("observer1")
    observer2 = my_add_observer("observer2")
    observer3 = my_add_observer("observer3")
    observer4 = my_add_observer("observer4")
    observer5 = my_add_observer("observer5")
    
    astronomer1 = my_add_astronomer("astronomer1")
    astronomer2 = my_add_astronomer("astronomer2")
    astronomer3 = my_add_astronomer("astronomer3")
    
    occult1 = my_add_occultation(astronomer1)
    occult2 = my_add_occultation(astronomer1)
    occult3 = my_add_occultation(astronomer1)
    occult4 = my_add_occultation(astronomer1)
    occult5 = my_add_occultation(astronomer1)
    occult6 = my_add_occultation(astronomer2)
    occult7 = my_add_occultation(astronomer2)
    past_occult1 = my_add_occultation(astronomer2, False)
    past_occult2 = my_add_occultation(astronomer3, False)
    past_occult3 = my_add_occultation(astronomer3, False)
    
    equipment1 = my_add_equipment(observer1)
    equipment2 = my_add_equipment(observer1)
    equipment3 = my_add_equipment(observer1)
    equipment4 = my_add_equipment(observer2)
    equipment5 = my_add_equipment(observer2)
    equipment6 = my_add_equipment(observer3)
    equipment7 = my_add_equipment(observer4)
    
    subscription1 = my_add_subscription(occult1, observer1)
    subscription2 = my_add_subscription(occult1, observer2)
    subscription3 = my_add_subscription(occult2, observer1)
    subscription4 = my_add_subscription(occult2, observer2)
    subscription5 = my_add_subscription(occult2, observer3)
    subscription6 = my_add_subscription(occult3, observer4)
    
    result1 = my_add_result(past_occult1, equipment1)
    result2 = my_add_result(past_occult1, equipment2)
    result3 = my_add_result(past_occult1, equipment3)
    result4 = my_add_result(past_occult2, equipment3)
    
    pass
    
"""
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
"""

if __name__ == "__main__":
    print "Starting populate script"
    populate()

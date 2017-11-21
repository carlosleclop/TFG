from django.contrib import admin
from transitweb.models import *

admin.site.register(Subscription)
admin.site.register(Equipment)
admin.site.register(Location)
admin.site.register(Occultation)
admin.site.register(UserObserver)
admin.site.register(UserAstronomer)
admin.site.register(Profile)
admin.site.register(Result)
admin.site.register(Notification)

# Register your models here.

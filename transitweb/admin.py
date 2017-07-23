from django.contrib import admin
from transitweb.models import *

admin.site.register(Subscription)
admin.site.register(Telescope)
admin.site.register(Location)
admin.site.register(Occultation)
admin.site.register(UserObserver)
admin.site.register(UserAstronomer)
admin.site.register(Profile)

# Register your models here.

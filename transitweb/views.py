from transitweb.models import *
from transitweb.forms import *

import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.utils.translation import ugettext as _

def initialize_context(request):
    context_dict = {}
    occultation_list = Occultation.objects.order_by("-datePrediction")[:20]

    context_dict["occultations"] = occultation_list

    if request.user.is_authenticated():
    #user = get_user(request)
        userObserver = get_UserObserver_from_request(request)
        userAstronomer = get_UserAstronomer_from_request(request)

        notifs = Notification.objects.filter(receiver = request.user)
        notifs_unread = notifs.filter(read = False)
        notifs_read = notifs.filter(read = True)
        context_dict["notifications_unread"] = notifs_unread
        #context_dict["notifications_unread"] = notifs_unread
        context_dict["notifications_read"] = notifs_read

        context_dict["notifications"] = notifs
        context_dict["notifications_count"] = len(notifs)

        if userObserver != None:
            context_dict["userObserver"] = userObserver
        if userAstronomer != None:
            context_dict["userAstronomer"] = userAstronomer

    return context_dict

def standard_index(request):
    context_dict = initialize_context(request)

    user_list = UserObserver.objects.order_by("-website")[:20]
    context_dict["users"] = user_list

    return context_dict

def index(request):
    context_dict = standard_index(request)
    return render(request, "transitweb/index.html", context_dict)

def index_nice_alert(request, alert):
    context_dict = standard_index(request)
    context_dict["a_nice_alert"] = alert
    return render(request, "transitweb/index.html", context_dict)

def index_alert(request, alert):
    context_dict = standard_index(request)
    context_dict["an_alert"] = alert
    return render(request, "transitweb/index.html", context_dict)

@login_required
def workspace_observer(request):
    context_dict = initialize_context(request)
    all_occultations = Occultation.objects.order_by("-datePrediction").reverse()
    context_dict["next_occultations"] = Occultation.objects.filter(datePrediction__gte = now()).order_by("-datePrediction").reverse()
    context_dict["near_occultations"] = Occultation.objects.order_by("-datePrediction").reverse()
    context_dict["past_occultations"] = Occultation.objects.filter(datePrediction__lte = now()).order_by("-datePrediction")
    context_dict["subs_occultations"] = Occultation.objects.filter(usersGo=context_dict.get("userObserver")).order_by("-datePrediction").reverse()
    context_dict["all_occultations"] = Occultation.objects.order_by("-datePrediction").reverse()
    return render(request, "workspace/observer.html", context_dict)

@login_required
def workspace_astronomer(request):
    context_dict = initialize_context(request)

    userAstronomer = context_dict.get("userAstronomer")
    if userAstronomer != None:
        context_dict["own_occults"] = Occultation.objects.filter(reporter = userAstronomer)
        return render(request, "workspace/astronomer.html", context_dict)

    return index_alert(request, "We are sorry, only authorized accounts can perform this action")

@login_required
def add_occult(request):
    context_dict = initialize_context(request)

    userAstronomer = get_UserAstronomer_from_request(request)
    # HTTP POST
    if userAstronomer == None:
        return index_alert(request, "We are sorry, only authorized accounts can perform this action")
    else:
        if request.method == "POST":
            form = OccultationForm(request.POST, request.FILES)

            if form.is_valid():
                ocu = form.save(commit=False)
                ocu.reporter = userAstronomer
                ocu.save()
                Notification.objects.send_notification_to_observers(
                        link = "/occultation/%s" % str(ocu.id))
                return index(request)
            else:
                print form.errors
        else:
            form = OccultationForm()

        context_dict["form"] = form
        return render(request, "management/add_occult.html", context_dict)

@login_required
def add_equipment(request):
    context_dict = initialize_context(request)

    userObserver = get_UserObserver_from_request(request)
    # HTTP POST
    if userObserver != None:
        if request.method == "POST":
            form = EquipmentForm(request.POST)
            # valid form?
            if form.is_valid():
                tel = form.save(commit=False)
                tel.user = userObserver
                tel.save()

                return HttpResponseRedirect('%s'%(reverse('workspace_observer')))
            else:
                print form.errors
        else:
            form = EquipmentForm()

        context_dict["form"] = form
        return render(request, "management/add_equipment.html", context_dict)
    else:
        return index_alert(request, "Error: you are not an observer.")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('')

def get_UserObserver_from_request(request):
    user = request.user
    for u in UserObserver.objects.all():
        if user == u.user:
            return u
    return None

def get_UserAstronomer_from_request(request):
    user = request.user
    for u in UserAstronomer.objects.all():
        if user == u.user:
            return u
    return None

@login_required
def user_profile(request):
    context_dict = initialize_context(request)
    return render(request, "accounts/profile.html", context_dict)

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'accounts/login.html', {})

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            default_observer = UserObserver()
            default_observer.user = user
            default_observer.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True
            return index_nice_alert(request, "Welcome to Transitweb! You have been registered sucessfully.")

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(
            request,
            'accounts/register.html',
            {
                'user_form': user_form,
                'profile_form': profile_form,
                'registered': registered
            })

def occult_page(request, occult_id):
    context_dict = initialize_context(request)

    userObserver = get_UserObserver_from_request(request)
    userAstronomer = get_UserAstronomer_from_request(request)
    occultation = get_object_or_404(Occultation, id=occult_id)

    context_dict["occultation"] = occultation

    if request.method == 'GET':
        userObserver = get_UserObserver_from_request(request)
        if (userObserver != None):
            if request.GET.get("action", None) == "subscribe":
                occultation.usersGo.add(userObserver)
            elif request.GET.get("action", None) == "unsubscribe":
                try:
                    occultation.usersGo.remove(userObserver)
                except Exception:
                    pass
            for u in occultation.usersGo.all():
                if u == userObserver:
                    context_dict["subscribed"] = True
        if (userAstronomer != None):
            context_dict["attendees"] = occultation.usersGo.all()

            json_data = equipments_to_json(context_dict["attendees"])
            context_dict["json_data"] = json_data

    return render(request, "transitweb/occult.html", context_dict)

def equipments_to_json(attendees):
    json_object = []
    for attendee in attendees:
        attendee_object = {}
        attendee_object["attendee"] = attendee.user.username
        attendee_object["equipments"] = []
        for equipment in attendee.equipment_set.all():
            coord_object = {}
            coord_object["lat"] = str(equipment.latitude)
            coord_object["lng"] = str(equipment.longitude)
            attendee_object["equipments"].append(coord_object)
        json_object.append(attendee_object)
    print json_object
    return json.dumps(json_object)

@login_required
def subscribe_occult(request, occult_id):
    context_dict = initialize_context(request)

    occultation = get_object_or_404(Occultation, id=occult_id)
    userObserver = get_UserObserver_from_request(request)
    if (userObserver != None):
        occultation.usersGo.add(userObserver)
    else:
        context_dict["an_alert"] = "Sorry, you cannot subscribe an event if you do not have equipment"
    context_dict["occultation"] = occultation
    return "ok"
    #render(request, "transitweb/occult.html", context_dict)

    try:
        occultation = Occultation.objects.get(id=occult_id)
        context_dict["occultation"] = occultation

        userObserver = get_UserObserver_from_request(request)
        if userObserver != None:
            if userObserver.equipment != None:
                equipment = userObserver.equipment

                subs = Subscription.objects.create(
                        occultation = occultation,
                        equipment = equipment,
                        additionalInfo = "Created")
                context_dict["subs"] = subs

            else:
                context_dict["an_alert"] = "Sorry, you cannot subscribe an event if you do not have equipment"
        else:
            context_dict["an_alert"] = "Sorry, you cannot subscribe an event if you are not an observer"

    except Occultation.DoesNotExist:
        pass

    return render(request, "transitweb/occult.html", context_dict)

@login_required
def delete_equipment(request, equipment_id):
    context_dict = initialize_context(request)
    user = request.user
    userObserver = get_UserObserver_from_request(request)

    if userObserver != None:
        try:
            equipment = Equipment.objects.filter(id=equipment_id)[0]
            equipment.delete()

            return HttpResponseRedirect('%s'%(reverse('user_profile')))
        except Exception as e:
            an_alert = "Unexpected error: " + str(e)
    else:
        an_alert = "You are no an observer"

    return index_alert(request, an_alert)

@login_required
def edit_equipment(request, equipment_id):
    context_dict = initialize_context(request)
    user = request.user
    userObserver = get_UserObserver_from_request(request)
    if userObserver != None:
        try:
            equipment = Equipment.objects.filter(id=equipment_id)[0]

            if request.method == 'POST':
                form = EditEquipmentForm(request.POST)
                if form.is_valid():
                    equipment.delete()
                    equipment = form.save(commit=False)
                    equipment.user = userObserver
                    equipment.save()

                    return HttpResponseRedirect('%s'%(reverse('workspace_observer')))

            else:
                form = EditEquipmentForm(
                        initial={'mobile': equipment.mobile,
                                 'country': equipment.country,
                                 'latitude': equipment.latitude,
                                 'longitude': equipment.longitude,
                                 'additionalInfo': equipment.additionalInfo})

                context_dict["form"] = form
                context_dict["equipment_id"] = equipment_id

                return render(request, "accounts/edit_equipment.html", context_dict)

        except Exception as e:
            an_alert = "Unexpected error: " + str(e)
    else:
        an_alert = "You are not an observer"

    return index_alert(request, an_alert)

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            profile.delete()
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            return HttpResponseRedirect('%s'%(reverse('user_profile')))

    else:
        form = EditProfileForm(
                initial={'website': profile.website,
                         'birth_date': profile.birth_date,
                         'country': profile.country,
                         'phone': profile.phone,
                         'public': profile.public})

        context = {
            "form": form
        }
        return render(request, "accounts/edit_profile.html", context)

def see_profile(request, username):
    context = initialize_context(request)
    context["other_user"] = get_object_or_404(User, username=username)
    return render(request, "profile/base_profile.html", context)

@login_required
def add_result(request, occult_id, equipment_id):
    context_dict = initialize_context(request)
    context_dict["occult_id"] = occult_id
    context_dict["equipment_id"] = equipment_id
    equipment = get_object_or_404(Equipment, id=equipment_id)
    occult = get_object_or_404(Occultation, id=occult_id)

    if request.method == 'POST':
        form = AddResultForm(data=request.POST)

        if form.is_valid():

            result_object = form.save(commit = False)
            result_object.equipment = equipment
            result_object.occultation = occult
            result_object.save()
            #occult_page(request, occult_id)
            #return (request, 'transitweb/occult_id.html', context_dict)
            return workspace_observer(request)
            #return HttpResponseRedirect('%s/%s'%(reverse('occultation'), str(occult_id)) )

        else:
            print result.errors

    else:
        form = AddResultForm()

    context_dict["form"] = form
    # Render the template depending on the context.
    return render(request, 'management/add_result.html', context_dict)

@login_required
def see_result(request, result_id):
    context_dict = initialize_context(request)

    result = get_object_or_404(Result, id=result_id)
    occultation = result.occultation
    equipment = result.equipment
    uploader = equipment.user

    context_dict["result"] = result
    context_dict["occultation"] = occultation
    context_dict["equipment"] = equipment
    context_dict["uploader"] = uploader

    return render(request, 'transitweb/result.html', context_dict)

@login_required
def see_notifications(request):
    context_dict = initialize_context(request)

    return render(request, 'management/notifications.html', context_dict)

@login_required
def mark_as_read(request):
    notif_id = None
    if request.method == "GET":
        notif_id = request.GET.get("notif_id")

    if notif_id:
        notif = Notification.objects.get(id = int(notif_id))
        notif.read = True
        notif.save()

    return None

@login_required
def remove_notification(request):
    notif_id = None
    if request.method == "GET":
        notif_id = request.GET.get("notif_id")

    if notif_id:
        notif = Notification.objects.get(id = int(notif_id))
        notif.delete()
    return None

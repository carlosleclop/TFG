from django.shortcuts import render
from transitweb.models import *
from transitweb.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

def initialize_context(request):
    context_dict = {}
    userObserver = get_UserObserver_from_request(request)
    userAstronomer = get_UserAstronomer_from_request(request)
    occultation_list = Occultation.objects.order_by("-datePrediction")[:20]

    if userObserver != None:
        context_dict["userObserver"] = userObserver
    if userAstronomer != None:
        context_dict["userAstronomer"] = userAstronomer
    context_dict["occultations"] = occultation_list

    return context_dict

def standard_index(request):
    context_dict = initialize_context(request)

    user_list = UserObserver.objects.order_by("-website")[:20]
    context_dict["users"] = user_list

    return context_dict

def index(request):
    context_dict = standard_index(request)
    return render(request, "transitweb/index.html", context_dict)

def index_alert(request, alert):
    context_dict = standard_index(request)
    context_dict["an_alert"] = alert

    return render(request, "transitweb/index.html", context_dict)

@login_required
def workspace_observer(request):
    context_dict = initialize_context(request)
    return render(request, "workspace/observer.html", context_dict)

@login_required
def workspace_astronomer(request):
    context_dict = initialize_context(request)
    return render(request, "workspace/astronomer.html", context_dict)

@login_required
def add_occult(request):
    userAstronomer = get_UserAstronomer_from_request(request)
    # HTTP POST
    if userAstronomer == None:
        return index_alert(request, "We are sorry, only authorized accounts can perform this action")
    else:
        if request.method == "POST":
            form = OccultationForm(request.POST)

            if form.is_valid():
                ocu = form.save(commit=False)
                ocu.save()
                return index(request)
            else:
                print form.errors
        else:
            form = OccultationForm()

        return render(request, "management/add_occult.html", {"form": form})

@login_required
def add_telescope(request):
    userObserver = get_UserObserver_from_request(request)
    # HTTP POST
    if userObserver != None:
        if request.method == "POST":
            form = TelescopeForm(request.POST)
            # valid form?
            if form.is_valid():
                tel = form.save(commit=False)
                tel.user = userObserver
                tel.save()

                return HttpResponseRedirect('%s'%(reverse('user_profile')))
            else:
                print form.errors
        else:
            form = TelescopeForm()

        return render(request, "management/add_telescope.html", {"form": form})
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
    if context_dict.get("userObserver") != None:
        return render(request,
                "accounts/profile_observer.html",
                context_dict)
    elif context_dict.get("userAstronomer") != None:
        return render(request,
                "accounts/profile_astronomer.html",
                context_dict)
    return render(request, "accounts/base_profile.html", context_dict)

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

            """
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            """
            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'accounts/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

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

    return render(request, "transitweb/occult.html", context_dict)

@login_required
def subscribe_occult(request, occult_id):
    context_dict = initialize_context(request)

    occultation = get_object_or_404(Occultation, id=occult_id)
    userObserver = get_UserObserver_from_request(request)
    if (userObserver != None):
        occultation.usersGo.add(userObserver)
    else:
        context_dict["an_alert"] = "Sorry, you cannot subscribe an event if you do not have a telescope"
    context_dict["occultation"] = occultation
    return "ok"
    #render(request, "transitweb/occult.html", context_dict)

    try:
        occultation = Occultation.objects.get(id=occult_id)
        context_dict["occultation"] = occultation

        userObserver = get_UserObserver_from_request(request)
        if userObserver != None:
            if userObserver.telescope != None:
                telescope = userObserver.telescope

                subs = Subscription.objects.create(
                        occultation = occultation,
                        telescope = telescope,
                        additionalInfo = "Created")
                context_dict["subs"] = subs

            else:
                context_dict["an_alert"] = "Sorry, you cannot subscribe an event if you do not have a telescope"
        else:
            context_dict["an_alert"] = "Sorry, you cannot subscribe an event if you are not an observer"

    except Occultation.DoesNotExist:
        pass

    return render(request, "transitweb/occult.html", context_dict)

@login_required
def delete_telescope(request, telescope_id):
    context_dict = initialize_context(request)
    user = request.user
    userObserver = get_UserObserver_from_request(request)

    if userObserver != None:
        try:
            telescope = Telescope.objects.filter(id=telescope_id)[0]
            telescope.delete()

            return HttpResponseRedirect('%s'%(reverse('user_profile')))
        except Exception as e:
            an_alert = "Unexpected error: " + str(e)
    else:
        an_alert = "You are no an observer"

    return index_alert(request, an_alert)

@login_required
def edit_telescope(request, telescope_id):
    context_dict = initialize_context(request)
    user = request.user
    userObserver = get_UserObserver_from_request(request)
    if userObserver != None:
        try:
            telescope = Telescope.objects.filter(id=telescope_id)[0]

            if request.method == 'POST':
                form = EditTelescopeForm(request.POST)
                if form.is_valid():
                    telescope.delete()
                    telescope = form.save(commit=False)
                    telescope.user = userObserver
                    telescope.save()

                    return HttpResponseRedirect('%s'%(reverse('user_profile')))

            else:
                form = EditTelescopeForm(
                        initial={'mobile': telescope.mobile,
                                 'country': telescope.country,
                                 'latitude': telescope.latitude,
                                 'longitude': telescope.longitude,
                                 'additionalInfo': telescope.additionalInfo})

                context_dict["form"] = form
                context_dict["telescope_id"] = telescope_id

                return render(request, "accounts/edit_telescope.html", context_dict)

        except Exception as e:
            an_alert = "Unexpected error: " + str(e)
    else:
        an_alert = "You are no an observer"

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

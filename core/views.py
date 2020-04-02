from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from random import randrange
from .models import *
from django.db.models import Q
from .forms import Create_Event_Form, CustomUserCreationForm, UserProfile_Form, EditProfileForm


def view_404(request, *e):
    return render(request, 'core/404.html')


def search(request):
    q = request.GET.get('q')
    if q:
        events = Event.objects.filter(Q(city__icontains = q) |
                                     Q(event_name__icontains = q)|
                                     Q(event_description__icontains = q)
                                     ).distinct().order_by('date')
        qtty = events.count()
        paginator = Paginator(events, 5)
        page = request.GET.get('page')
        events = paginator.get_page(page)
        #messages.success(request,f'Nous avons trouvé {qtty} événements {event}')
        return render(request, "core/chercher-evenement.html", {"events":events})
        #else:
        #    messages.error(request,f'Nos lutins n\'ont pas compris')
        #    return render(request, "core/chercher-evenement.html")
    else:
        messages.success(request, "todos los eventos de tu ciudad:")
        return (search_event(request))


        #else:
        #    messages.error(request,"Else de if q: devuelvo a \"search_event\" ")
        #    return redirect( "search_event")



def home(request):
    sports = [
            'jouer au Foot',
            'te faire un Golf',
            'jouer au Tennis',
            'te faire un Jogging',
        ]
    xrandom = randrange(0, len(sports), 1)
    randomsport = str(sports[xrandom])
    return render(request, 'core/index.html', {'randomsport': randomsport})


def profile(request):
    id = request.user.id
    try:
        user=User.objects.get(pk=id)
        userprofile = UserProfile.objects.get(user_id=id)
        context = {'utilisateur': user, 'userprofile': userprofile}
        return render(request, 'core/profile.html', context)
    except User.DoesNotExist:
        messages.error("Cet utilisateur n'existe plus")
        return redirect('profile')


def visit_profile(request, id):
    try:
        user = User.objects.get(pk=id)
        userprofile = UserProfile.objects.get(user_id=id)
        context = {'utilisateur': user, 'userprofile': userprofile}
        return render(request, 'core/profile.html', context)
    except User.DoesNotExist:
        messages.error(request, "Cet utilisateur n'existe pas")
        return redirect('profile')
    except Entry.MultipleObjectsReturned:
        messages.error(request, "Plusieurs utilisateurs trouvés")
        return redirect('profile')


def edit_profile(request):
    if request.method == 'POST':
        try:
            form = EditProfileForm(request.POST, instance=request.user)
            profileForm = UserProfile_Form(request.POST,request.FILES, instance=request.user.userprofile)
            if form.is_valid() and profileForm.is_valid():
                form.save(commit=False)
                profileForm.save(commit=True)
                form.save(commit=True)
                messages.success(request, 'Ton profil a été modifié :)')
                return redirect('profile')
        except Exception as e:
            error = str(e)
            messages.error(
                        request,
                        f"Oops!!! nos lutins ont fait une betise. {error}"
                    )
    else:
        form = EditProfileForm(instance=request.user)
        profileForm = UserProfile_Form(instance=request.user.userprofile)
        context = {'form': form, 'profileForm': profileForm }
        return render(request, 'core/edit-profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ton mot de passe a été changé :)")
            return redirect(request, 'core/profile')

    else:
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'core/change-password.html', context)


def my_events(request, id):
    event = get_object_or_404(Event, id=id)
    if event:
        events = Event.objects.filter(owner=request.user.id).order_by('date')
        qtty = events.count()
        paginator = Paginator(events, 5)
        page = request.GET.get('page')
        events = paginator.get_page(page)
        context = {'events': events}
        return render(request, "core/liste-evenements.html", {"events":events})


def validate(request, id):
    event = Event.objects.get(id=id)
    if event.owner_id == request.user.id:
        events = EventJoin.objects.filter(event=id)
        context = {'events': events}
        return render(request, "core/valider-demandes.html", context)
    else:
        messages.error(request, f'Cet événement ne t\'appartiens pas!')
        return redirect('index')


def accept(request, guest_id, event_id):
    guest = UserProfile.objects.get(user_id=guest_id)
    ev = EventJoin.objects.get(id=event_id)
    ev.accepted = True
    ev.save()
    if (ev.accepted):
        messages.success(request, f'{guest} a été accepté à ton événement')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



#Muestro los eventos en la ciudad del usuario:
def search_event(request):
    user_id = request.user.id
    u=UserProfile.objects.get(user_id=user_id)
    events = Event.objects.filter(city = u.city).order_by('date')
    context = {'events':events}
    return render (request, 'core/chercher-evenement.html', context)


#class SearchEventList(ListView):
#    model = Event
#    template_name = 'core/chercher-evenement.html'
#    paginate_by = 5


def apply(request, id):
    user_name = request.user.first_name
    user_id = request.user.id
    if request.method == 'GET':
        try:
            # event =  get_object_or_404(Event, pk=id) #Event.objects.get(id=id)
            guest = UserProfile.objects.get(user_id=user_id)
            # ICI CA MARCHEev = EventJoin(event=Event.objects.get(id=id), guest=guest)
            ev = EventJoin(event=Event.objects.get(id=id), guest=guest)
            ev.save()
            messages.success(request, f"{user_name}, ta demande a été envoyée! :)")
            return redirect('search_event')
        except Exception as e:
            error = str(e)
            if "UNIQUE" in error:
                messages.error(
                                request,
                                "Oops!!! tu as déjà postulé à cet événement"
                            )
                return redirect('search_event')
            else:
                messages.error(
                                request,
                                f"Oops!!! nos lutins ont fait une betise. {error}"
                            )
                return redirect('search_event')

        #ESTO FUNCIONA!!
        #try:
        #    if request.method == 'GET':
        #        #event =  get_object_or_404(Event, pk=id) #Event.objects.get(id=id)
        #        guest = UserProfile.objects.get(user_id=user_id)
        #        # ICI CA MARCHEev = EventJoin(event=Event.objects.get(id=id), guest=guest)
        #        ev = EventJoin(event=Event.objects.get(id=id), guest=guest)
        #        ev.save()
        #        return HttpResponse(user_name+"  Application enregistrée")
        #except Exception as e:
        #    error = e
        #    return HttpResponse(e,"Ya se registro")


@login_required
def create_event(request):
    data = {'form': Create_Event_Form()}
    if request.method == 'POST':
        form = Create_Event_Form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user  ############
            post.save()
            messages.success(
                                request,
                                f'Merci {request.user}! ton événement a été crée <3'
                        )
            return redirect('index')
        else:
            data['form'] = form
            messages.error(request, form.errors)
            messages.error(
                            request,
                            f'Oops {request.user}! ton événement n\'a pas été crée :C'
                        )
    return render(request, 'core/creer-evenement.html', data)


def create_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        ProfileForm = UserProfile_Form(request.POST, request.FILES)
        if form.is_valid() and ProfileForm.is_valid():
            user = form.save()
            profile = ProfileForm.save(commit=False)
            profile.user = user
            profile.save()
    else:
        form = CustomUserCreationForm()
        ProfileForm = UserProfile_Form()
    context = {'form': form, 'profileForm': ProfileForm}
    return render(request, 'registration/register.html', context)

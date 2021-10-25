from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver as rciver
from rest_framework.authtoken.models import Token





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_description = models.TextField("Bio",blank = True, null = False)
    address =  models.CharField("Address",max_length = 200, blank = False, null = False)
    city =  models.CharField("Ville",max_length = 100, blank = False, null = False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='/avatars/default.png')#
    is_the_owner = models.BooleanField('Annonceur', default=False)
    is_coming = models.BooleanField('Asistant', default=False)


    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    def __str__(self):
        return(self.user.first_name)



class Event(models.Model):

    created_on = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            null=True,
            related_name='event_owner'
        )
    event_assisters = models.ManyToManyField(
                                UserProfile,
                                through='EventJoin',
                                related_name='event_assisters'
        )
    event_name = models.CharField(
                                "Title",
                                max_length = 100,
                                blank = False,
                                null = False
        )
    event_description = models.TextField(
                                "Description de l'événement",
                                blank = True,
                                null = False
        )
    nber_of_places = models.IntegerField(
                                'Combien de personnes cherchez-vous?',
                                blank=False,
                                null=False,
                                default=1
        )
    event_address = models.CharField(
                                "Address",
                                max_length = 1024,
                                blank = False,
                                null = False
        )

    zip_code = models.CharField("Code postal", max_length=6,blank = False, null = False)
    city = models.CharField("Ville",max_length = 100, blank = False, null = False)
    date = models.DateField("Date de l'événement",blank = False, null = False   )
    time = models.TimeField("Heure de l'événement",blank = False, null = False)
    is_active = models.BooleanField('Evénement Actif', default=True)
    is_full = models.BooleanField('Evénement complet', default=False)

    class Meta:
        verbose_name = "Evénement"
        verbose_name_plural = "Evénements"
    def __str__(self):
        return(self.event_name)

    def is_the_owner(self):
        return (Event.owner == self.id)

class EventJoin(models.Model):
    event = models.ForeignKey(
                    Event, null=False,
                    blank=False,
                    verbose_name='événement',
                    on_delete=models.PROTECT
        )
    guest = models.ForeignKey(
                    UserProfile,
                    null=False,
                    blank=False,
                    verbose_name='guest',
                    on_delete=models.PROTECT
        )
    accepted = models.BooleanField(default=False, null=True, blank=True, verbose_name='A assisté')
    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        #constraints = [
        #    models.UniqueConstraint(fields=['event', 'guest'], name='invité ')
        #    ]
    def __str__(self):
        return self.event.event_name


class Message(models.Model):
    sender = models.ForeignKey(
                    UserProfile,
                    null=True,
                    on_delete = models.SET_NULL,
                    related_name='sender'
        )
    receiver = models.ForeignKey(
                    UserProfile,
                    null=True,
                    on_delete = models.SET_NULL,
                    related_name='receiver'
        )
    text = models.CharField('Message:', blank = True, null = False, max_length=500)
    sent = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    def __str__(self):
            return(str(self.sender))




class Evaluation(models.Model):
    evaluator = models.ForeignKey(
                    UserProfile,
                    null=True,
                    on_delete = models.SET_NULL,
                    related_name='evaluator'
        )
    evaluation_text = models.CharField(
                    "Evaluation"
                    ,max_length = 1024,
                    blank = True,
                    null = False
            )
    evaluated_guy = models.ForeignKey(
                    UserProfile,
                    null=True,
                    on_delete = models.SET_NULL,
                    related_name='evaluated'
        )
    class Meta:
        verbose_name = "Evaluation"
        verbose_name_plural = "Evaluations"
    def __str__(self):
            return(str(self.evaluator))

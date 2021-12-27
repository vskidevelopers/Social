from django.db import models
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.template.defaultfilters import slugify
from .utils import generate_uuid_code

# Create your models here.

#Choices 
class Year_of_study(models.TextChoices):
    FIRST='first'
    SECOND= 'second'
    THIRD= 'third'
    FOURTH= 'fourth'
    FIFTH = 'fifth'
    SIXTH = 'sixth'

class Study_level(models.TextChoices):
    CERT ='certificate'
    DEGREE= 'degree'
    MASTERS= 'masters'
    PHD= 'doctrate'

class Frienship_status(models.TextChoices):
    FRIENDSHIP_SENT = "send"
    FRIENDSHIP_ACCEPTED ="accepted"


class ProfileManager(models.Manager):
    def get_profiles_available_for_invite(self, sender):
        profiles= Profiles.objects.all().exclude(user=sender)
        profile=Profiles.objects.get(user=sender)
        queryset= Friendship.objects.filter(Q(sender=profile)|Q(receiver=profile))
    
        accepted=set([])

        for friendship in queryset:
            if friendship.friendship_status =="accepted":
                accepted.add(friendship.sender)
                accepted.add(friendship.receiver)
        
        available=[profile for profile in profiles if profile not in accepted ]
        return available


    def get_profiles(self, user):
        profiles= Profiles.objects.all().exclude(user=user)
        return profiles

class Profiles(models.Model):
    """Model definition for Profiles."""

    # TODO: Define fields here
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    bio= models.TextField(max_length=500, blank=True, null=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    year_of_study=models.CharField(max_length=50, choices=Year_of_study.choices, blank=True, null=True) 
    course = models.CharField(max_length=200, blank=True, null=True)
    study_level =models.CharField(max_length=50, choices=Study_level.choices, default=Study_level.CERT) 
    friends = models.ManyToManyField(User, blank=True, related_name='friends' )
    avatar = models.ImageField(default="avatar.png",  upload_to="avatars/")
    slug = models.SlugField(unique=True, blank=True, max_length=500)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # instaciate the profile manager
    objects=ProfileManager()
    class Meta:
        """Meta definition for Profiles."""

        verbose_name = 'Profiles'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profiles."""
        return f"{self.user.username} - {self.created.strftime('%d-%m-%Y')}"

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()
    
    def get_created_date(self):
        return self.created.strftime('%d-%m-%Y')

    def get_display_bio(self):
        return str(self.bio[:20])
    
    def get_display_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_display_friends(self):
        friends = self.get_friends()
        friends_count=friends.count() - 1
        if friends_count == 0:
            friends_to_show = friends[0]
        elif friends_count>=2:
                friends_to_show = str(friends[0])+' and',    str(friends_count)+ " others"
        else:
            friends_to_show = friends[0]
        return friends_to_show
    

        
    def save(self, *args, **kwargs):
        """Save method for Profiles."""
        ex =False
        if self.first_name and self.last_name:
            slug= slugify(str(self.first_name)+" "+(self.last_name))
            ex = Profiles.objects.filter(slug=slug).exists()
            while ex:
                slug=slugify(slug+" "+ str(generate_uuid_code()))
                ex=Profiles.objects.filter(slug=slug).exists()
        else:
            slug = str(self.user.username)
        
        self.slug = slug
        super().save( *args, **kwargs)

class FriendshipManager(models.Manager):
    def friend_requests_recieved(self, receiver):
        queryset=Friendship.objects.filter(receiver=receiver, friendship_status="send")
        return queryset

class Friendship(models.Model):
    """Model definition for Friendship."""

    # TODO: Define fields here
    sender = models.ForeignKey(Profiles, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profiles, related_name="reciever", on_delete=models.CASCADE)
    friendship_status = models.CharField(max_length=50, choices=Frienship_status.choices)
    objects = FriendshipManager()
    class Meta:
        """Meta definition for Friendship."""
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'

    def __str__(self):
        return f"{self.sender.user}  &  {self.receiver.user} - {self.friendship_status}"


from django.db import models
from django.contrib.auth.models import User
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

    class Meta:
        """Meta definition for Profiles."""

        verbose_name = 'Profiles'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profiles."""
        return f"{self.user.username} - {self.created.strftime('%d-%m-%Y')}"

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

class Friendship(models.Model):
    """Model definition for Friendship."""

    # TODO: Define fields here
    sender = models.ForeignKey(Profiles, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profiles, related_name="reciever", on_delete=models.CASCADE)
    friendship_status = models.CharField(max_length=50, choices=Frienship_status.choices)
    class Meta:
        """Meta definition for Friendship."""
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'

    def __str__(self):
        return f"{self.sender}  &  {self.receiver} - {self.friendship_status}"


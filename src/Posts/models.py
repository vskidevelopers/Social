from django.db import models
from django.core.validators import FileExtensionValidator
from Profile.models import Profiles

# Create your models here.

# Like Choices
class Likes(models.TextChoices):
    LIKE ='like'
    UNLIKE= 'unlike'

class Post(models.Model):
    """Model definition for Post."""

    # TODO: Define fields here
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profiles, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='posts')
    class Meta:
        """Meta definition for Post."""

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-created',)

    def __str__(self):
        return str(self.content[:20])

    def get_likes_count(self):
        return self.liked.all().count()

    def get_comments_count(self):
        return self.comment_set.all().count()

class Comment(models.Model):
    """Model definition for Comment."""

    # TODO: Define fields here
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        """Meta definition for Comment."""

        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return str(self.pk)

class Like(models.Model):
    """Model definition for Like."""

    # TODO: Define fields here
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=Likes.choices, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        """Meta definition for Like."""

        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f"{self.user.user} - {self.post} - {self.value}"


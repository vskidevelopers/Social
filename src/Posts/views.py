from django.shortcuts import redirect, render
from .models import Post, Like, Comment
from Profile.models import Profiles
from .forms import *
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
def post_comment_list_view(request):
    queryset = Post.objects.all()
    profile = Profiles.objects.get(user=request.user)
    comment_form = CommentModelForm()
    post_form =PostModelForm()
    post_added = False

    if "submit_comment_form" in request.POST:
        comment_form=CommentModelForm(request.POST)
        if comment_form.is_valid():
            draft_comment=comment_form.save(commit=False)
            draft_comment.user=profile
            draft_comment.post=Post.objects.get(id=request.POST.get('post_id'))
            draft_comment.save()
            draft_comment=CommentModelForm()


    if "submit_post_form" in request.POST:
        post_form= PostModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            draft= post_form.save(commit=False)
            draft.author= profile
            draft.save()
            post_form =PostModelForm()
            post_added = True

    context = {
        'posts':queryset ,
        'profile': profile,
        'post_form':post_form,
        'comment_form':comment_form,
        'post_added':post_added
    }

    return render(request, 'posts/main.html', context)

def like_unlike_post(request):
    if request.method == 'POST':
        post_id=request.POST.get('post_id')
        post=Post.objects.get(id = post_id)
        profile = Profiles.objects.get(user=request.user)

        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)
        
        like, created = Like.objects.get_or_create(user=profile, post_id =post_id)
        
        if not created:
            if like.value =="like":
                like.value="unlike"
            else:
                like.value ="like"
        else:
            like.value ="like"

            post.save()
            like.save()
    
    return redirect( 'post:post_view')


class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts/delete.html"
    success_url = reverse_lazy("post:post_view")

    def get_object(self, *args, **kwargs):
        pk=self.kwargs.get('pk')
        post=Post.objects.get(pk=pk)
        if post.author.user != self.request.user:
            messages.warning(self.request, "sorry pal, You cant do that. This aint your post! ")
        return post

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import ListView, TemplateView
from .models import Post, Comment
from .forms import CommentForm, SignupForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic.edit import UpdateView, DeleteView
from random import sample
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class IndexView(ListView):
    template_name = 'forumapp/index.html'
    context_object_name = 'random_posts'
    paginate_by = 3

    def get_queryset(self):
        all_posts = Post.objects.all()
        return sample(list(all_posts), 3)

class PostList(ListView):
    model = Post
    template_name = 'forumapp/post_list.html'
    context_object_name = "post_list"
    paginate_by = 6
    queryset = Post.objects.filter(status=1).order_by('?')[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.all()
    comment_form = CommentForm()

    return render(
        request,
        "forumapp/post_detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
        # Handle the case where the form is not valid
        # You might want to add some error handling or messages for the user
    else:
        # Handle the case where the request method is not POST
        pass

    return redirect('post_detail', slug=post.slug)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'forumapp/signup.html', {'form':form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'forumapp/create_post.html', {'form': form})

# The following two views are collected from duski.harap on steemit.com - for full reference, see README.md   

class OwnerProtectMixin(object):
    def dispatch(self, request, *args, **kwargs):
        objectUser = self.get_object()
        if objectUser.user != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)
 
@login_required
class PostUpdateView(OwnerProtectMixin, UpdateView):
    model = Post
    fields = ['title', 'content',]
    template_name = 'forumapp/post_update_form.html'

    def get_success_url(self, **kwargs):
	    return reverse_lazy('forum-detail', kwargs={'slug' : self.object.slug})

@login_required
class PostDeleteView(SuccessMessageMixin, OwnerProtectMixin, DeleteView):
	model = Post
	success_url = '/forumapp'
	success_message = 'Forum was successfully deleted'

class CommentUpdateView(OwnerProtectMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'forumapp/update_comment.html'

class FamilyView(generic.ListView):
    template_name = 'forumapp/family.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(category='family', status=1).order_by('-created_on')

class PastimesView(generic.ListView):
    template_name = 'forumapp/pastimes.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(category='pastimes', status=1).order_by('-created_on')
    
class CareerView(generic.ListView):
    template_name = 'forumapp/career.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(category='career', status=1).order_by('-created_on')
    
class WallOfComplaintsView(generic.ListView):
    template_name = 'forumapp/wall_of_complaints.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(category='wall_of_complaints', status=1).order_by('-created_on')
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post
from .forms import CommentForm, SignupForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "forumapp/index.html"
    paginate_by = 6

    def get_queryset(self):
        # Fetch three random posts for each slide
        # posts = Post.objects.filter(status=1).order_by('?')[:3]
        posts = Post.objects.filter(status=1)
        total_posts = posts.count()
        
        if total_posts < 3:
            # Duplicate the posts to fill the carousel
            posts = Post.objects.filter(status=1).order_by('?')[:3] * (3 // total_posts + 1)
        else:
            posts = Post.objects.filter(status=1).order_by('?')[:3]

        return posts


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
            # Optionally, you can redirect to the post detail page or any other page
            return redirect('post_detail', slug=post.slug)
        # Handle the case where the form is not valid
        # You might want to add some error handling or messages for the user
    else:
        # Handle the case where the request method is not POST
        pass

    # You can customize this part based on your requirements
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
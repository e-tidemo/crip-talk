from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post
from .forms import CommentForm, SignupForm
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
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.
    ``comments``
        A list of :model:`blog.Comment` objects for the post.
    ``comment_form``
        An instance of :form:`blog.CommentForm` for adding new comments.

    **Template:**

    :template:`blog/post_detail.html`
    """

    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:  # Check if the user is logged in
            comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', slug=post.slug)
        else:
            # Handle the case where the user is not logged in (maybe redirect to login page)
            # You can customize this part based on your requirements
            pass
    else:
        comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form':form})
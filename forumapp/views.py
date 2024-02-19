from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "forumapp/index.html"
    paginate_by = 6

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
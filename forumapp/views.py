from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.views.generic import ListView, TemplateView
from .models import Post, Comment, TermsAndConditions
from .forms import CommentForm, SignupForm, PostForm, ReportForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.views.generic.edit import UpdateView, DeleteView
from random import sample
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class IndexView(ListView):
    template_name = 'forumapp/index.html'
    context_object_name = 'random_posts'
    paginate_by = 3

    def get_queryset(self):
        all_posts = Post.objects.filter(status=1).exclude(slug='')
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

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.all()
    comment_form = CommentForm()

    return render( request, "forumapp/post_detail.html", {"post": post, "comments": comments, "comment_form": comment_form},)

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
#The following view is collected from skolo-online.medium - for full reference, see README.md
def signup(request):
    if request.method == 'GET':
        form  = SignupForm()
        context = {'form': form}
        return render(request, 'forumapp/signup.html', context)
    if request.method == 'POST':
        form  = SignupForm(request.POST)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, 'Account was created for ' + user)
        return redirect('home')
    else:
        print('Form is not valid')
        messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, 'forumapp/signup.html', context)
    
    return render(request, 'forumapp/signup.html', {'form':form})

def terms_and_conditions(request):
    terms = TermsAndConditions.objects.first()
    return render(request, 'forumapp/terms_and_conditions.html', {'terms': terms})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            if post.slug:  # Check if post.slug is not empty
                return redirect('post_detail', slug=post.slug)
            else:
                raise ValueError("Empty slug encountered when trying to create a post.")
    else:
        form = PostForm()

    return render(request, 'forumapp/create_post.html', {'form': form})

# The following two views are collected from duski.harap on steemit.com - for full reference, see README.md   

class OwnerProtectMixin(object):
    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)
 
@method_decorator(login_required, name='dispatch')
class PostUpdateView(OwnerProtectMixin, UpdateView):
    model = Post
    fields = ['title', 'content',]
    template_name = 'forumapp/post_update_form.html'
    context_object_name = 'post-edit'

    def get_success_url(self):
        post_slug = self.object.slug
        return reverse_lazy('post_detail', kwargs={'slug': post_slug})


@method_decorator(login_required, name='dispatch')
class PostDeleteView(SuccessMessageMixin, OwnerProtectMixin, DeleteView):
    model = Post
    context_object_name = 'delete-post'
    success_url = reverse_lazy('home')
    success_message = 'Post was successfully deleted'

@method_decorator(login_required, name='dispatch')
class CommentUpdateView(OwnerProtectMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'forumapp/update_comment.html'
    context_object_name = 'edit-comment'

    def get_success_url(self):
        post_slug = self.object.post.slug
        return reverse_lazy('post_detail', kwargs={'slug': post_slug})
    
@method_decorator(login_required, name='dispatch')
class CommentDeleteView(SuccessMessageMixin, OwnerProtectMixin, DeleteView):
    model = Comment
    context_object_name = 'delete-comment'
    success_message = 'Comment was successfully deleted'

    def get_success_url(self):
        post_slug = self.object.post.slug
        return reverse_lazy('post_detail', kwargs={'slug': post_slug})

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

# The search_results view is collected from Codemy.com on Youtube - see README.md for full reference 
def search_results(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)

        return render(request, 'forumapp/search_results.html', {'searched':searched, 'posts':posts})
    else:
        return render(request, 'forumapp/search_results.html', {})

def get_post_content_by_slug(post_slug):
    return "This is the content of the post with slug: " + post_slug

@login_required
def send_report_email(request, post_slug=None, comment_id=None):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender_email = request.user.email

            admin_email = 'elvira.d.tidemo@gmail.com'

            send_mail(
                subject,
                f"From: {sender_email}\n\n{message}",
                sender_email,
                [admin_email],
                fail_silently=False,
            )

            return render(request, 'success_template.html')  # Redirect to a success template
    else:
        form = ReportForm()

    if post_slug:
        # Retrieve the post content based on the slug
        post_content = get_post_content_by_slug(post_slug)
        # Set default values for the form
        form.fields['subject'].initial = 'Crip Talk report'
        form.fields['message'].initial = f'A report has been made on this post:\n\n{post_content}'

    return render(request, 'report_form_template.html', {'form': form})
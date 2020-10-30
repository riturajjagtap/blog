from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView,
                                    UpdateView, DeleteView)
from blogapp.models import  Post, Comment
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blogapp.forms import PostForm, CommentForm
from django.urls import reverse_lazy

#############################################################
# Views for Posts

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blogapp/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blogapp/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name ='blogapp/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


####################################
# Views for Comments
####################################

# Adding comment
@login_required
def add_comment_to_post(req, pk):
    post = get_object_or_404(Post, pk=pk)
    if req.method == 'POST':
        frm = CommentForm(req.POST)
        if frm.is_valid():
            comment = frm.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        frm = CommentForm()
    return render(req, 'blogapp/comment_form.html', {'form': frm})


# Approve comment
@login_required
def comment_approve(req, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

# Remove comment
@login_required
def comment_remove(req, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

# Publish Post
@login_required
def post_publish(req, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

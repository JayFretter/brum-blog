from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, CVSection
from .forms import PostForm, CVSectionForm

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(date_published__lte=timezone.now()).order_by('date_published')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.author = request.user
            post.date_published = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form, 'post_pk': 0, 'can_delete': False})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.author = request.user
            post.date_published = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post_pk': pk, 'can_delete': True})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        post.delete()
    return redirect('post_list')

def cv_show(request):
    cv_sections = CVSection.objects.all
    return render(request, 'blog/cv_show.html', {'cv_sections': cv_sections})

def cv_new(request):
    if request.method == "POST":
        form = CVSectionForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save()
            return redirect('cv_show')
    else:
        form = CVSectionForm()
    return render(request, 'blog/cv_edit.html', {'form': form, 'cv_section_pk': 0, 'can_delete': False})

def cv_edit(request, pk):
    cv_section = get_object_or_404(CVSection, pk=pk)
    if request.method == "POST":
        form = CVSectionForm(request.POST, instance=cv_section)
        if form.is_valid() and request.user.is_authenticated:
            cv_section.save()
            return redirect('cv_show')
    else:
        form = CVSectionForm(instance=cv_section)
    return render(request, 'blog/cv_edit.html', {'form': form, 'cv_section_pk': pk, 'can_delete': True})

def cv_delete(request, pk):
    cv_section = get_object_or_404(CVSection, pk=pk)
    if request.user.is_authenticated:
        cv_section.delete()
    return redirect('cv_show')
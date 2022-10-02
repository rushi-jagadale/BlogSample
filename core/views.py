from django.shortcuts import render, get_object_or_404, redirect
from core.models import Blog
from core.forms import BlogForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Blog
from django.contrib.auth.decorators import login_required
import os

# Create your views here.


@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('listing')
    else:
        form = BlogForm()
    return render(request, 'post.html', {'form': form})

@login_required
def listing(request):
    data = {
        "blogs": Blog.objects.filter(user=request.user)
    }
    if request.user.is_superuser: 
        data = {
        "blogs": Blog.objects.all()    }

    return render(request, "listing.html", data)

@login_required
def edit_blog(request, blog_id):
    if request.user.is_superuser: 
        blog = Blog.objects.get(id=blog_id)
    else:
        blog = Blog.objects.filter(user=request.user).get(id=blog_id)
   

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(blog.img) > 0:
                os.remove(blog.img.path)
            blog.img = request.FILES['img']
            blog.title = request.POST.get('title')
            blog.user = request.user
            blog.save()
            # messages.success(request, "Product Updated Successfully")
            return redirect('listing')
    data = {
        "blog": blog,
    }
    return render(request, "view_blog.html", data)

@login_required
def destroy(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect("listing")


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:

            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already taken..')

                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken ..')

                return redirect('register')

            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password2)
                user.save()
                messages.info(request, 'User Created')
                return redirect('login')
        else:
            messages.info(request, 'Password is missmatch')
            return redirect('register')
    else:

        return render(request, 'register.html')


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        # email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:

            auth.login(request, user)
            return redirect('listing')

        else:

            messages.info(request, 'invalid username and password')
            return redirect('login')
    else:

        return render(request, 'login.html')

    # return render(request,'login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

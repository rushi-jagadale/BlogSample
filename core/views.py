from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from core.models import Blog
from django.views.generic.edit import UpdateView 
from core.forms import BlogForm
from django.contrib.auth.models import User,auth
from django.contrib import messages


# Create your views here.

def listing(request):
    data = {
        "blogs": Blog.objects.filter(user= request.user)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    }

    return render(request, "listing.html", data)

def view_blog(request, blog_id):
    # blog = get_object_or_404(Blog, id=blog_id)
    blog = Blog.objects.filter(user= request.user)
    data = {
        "blog":blog,
    }

    return render(request, "view_blog.html", data)

def update(request, blog_id):
    blog = Blog.objects.filter(user= request.user).get(id = blog_id)
    form = BlogForm(request.POST, instance=blog)
    if form.is_valid():
        form.save()
        return redirect("listing")
    return render(request, "view_blog.html")


def destroy(request, blog_id):
    blog = Blog.objects.get(id = blog_id)
    blog.delete()
    return redirect("listing")   

def signup(request):
    if request.method == 'POST':             
        username = request.POST['username']
        email= request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:

            if User.objects.filter(username = username).exists():
                messages.info(request, 'username already taken..')
               
                return redirect('register')

            elif User.objects.filter(email = email).exists():
                messages.info(request, 'Email already taken ..')
                
                return redirect('register')
            
            else:
                user = User.objects.create_user(username = username,email=email,password = password2)
                user.save()
                messages.info(request,'User Created')
                return redirect('login')
        else:
            messages.info(request,'Password is missmatch')
            return redirect('register')        
    else:
                     
        return render(request,'register.html')

def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        # email = request.POST['email']
        password = request.POST['password']
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        user = auth.authenticate(username= username, password = password)

        if user is not None:

            auth.login(request, user)   
            return redirect('listing')

        else:

            messages.info(request, 'invalid username and password')
            return redirect('login')
    else:

        return render(request, 'login.html')

    # return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')        
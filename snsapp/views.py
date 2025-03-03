from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import SnsModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.

def signup_func(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username,'',password)
            return render(request,'signup.html',{'error':'登録完了'})

        except IntegrityError:
            return render(request,'signup.html',{'error':'このユーザー名はすでに使用されています'})
        
    return render(request,'signup.html',{})

def login_func(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) # ここで認証
        if user is not None:
            login(request,user)
            return redirect('list')
        else:
            return render(request, 'login.html', {'context':'ログイン失敗'})

    return render(request, 'login.html', {'context':'ログインしてください'})

@login_required
def list_func(request):
    object_list = SnsModel.objects.all()
    return render(request, 'list.html',{'object_list':object_list})

@login_required
def logout_func(request):
    logout(request)
    return redirect('login')

@login_required
def detail_func(request, pk):
    object = get_object_or_404(SnsModel, pk=pk)
    return render(request, 'detail.html', {'object':object})

@login_required
def good_func(request, pk):
    object = SnsModel.objects.get(pk = pk)
    object.good = object.good + 1
    object.save()
    return redirect('list')

@login_required
def read_func(request, pk):
    object = SnsModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in object.readtext:
        return redirect('list')
    else:
        object.read = object.read + 1
        object.readtext = object.readtext + ' ' + username
        object.save()
        return redirect('list')
    # return render(request, 'detail.html', {'object':object})

class create_func(CreateView):
    template_name = 'create.html'
    model = SnsModel
    fields = ('title', 'content', 'author', 'snsimage')
    success_url = reverse_lazy('list')


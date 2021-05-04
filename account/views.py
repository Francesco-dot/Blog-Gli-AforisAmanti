from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from .forms import PostForm
from django.utils import timezone
from .models import Post, UserIp
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from datetime import timedelta
from django.core import serializers
from django.contrib import messages
from .utils import sendTransaction
import hashlib

def LoginView(request):
    if request.user.is_authenticated:
        return redirect('message_board')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            lastIp = UserIp.objects.get(user=user)
            if not lastIp.ip == getIp(request):
                lastIp.ip = getIp(request)
                lastIp.save()
                messages.info(request, "Il tuo Ip è cambiato rispetto all'ultima sessione, fai attenzione")
            return redirect('message_board')
        else:
            messages.info(request, 'Nome utente o Password non corretti')

    return render(request, 'account/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('message_board')
    form = UserRegistrationForm(request.POST)
    modelIp = UserIp()
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        modelIp.user = User.objects.get(username=user)
        modelIp.ip = getIp(request)
        modelIp.save()
        messages.success(request,'Account creato con successo, benvenuto '+ user)
        return redirect('login')
    context = {'form':form}
    return render(request, 'account/register.html', context)

@login_required
def message_board(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'account/message_board.html', {'posts': posts})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.hash = hashlib.sha256(post.text.encode('utf-8')).hexdigest()
            post.txId = sendTransaction(post.hash)
            post.save()
            return redirect('message_board')
    else:
        form = PostForm()
    return render(request, 'account/post_edit.html', {'form':form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'account/post_detail.html', {'post': post})

@user_passes_test(lambda u: u.is_staff)
def staff_index(self):
    return render(self, 'account/staff_index.html')

@user_passes_test(lambda u: u.is_staff)
def num_post(request):
    num_post = dict(User.objects.values_list('username').annotate(Count('post')))
    return render(request, 'account/post_numbers.html', {'num_post' : num_post})

@login_required
def dashboard(request):
    return render(request,
    'account/message_board.html',
    {'section': 'dashboard'})

@login_required
def user_profile(request, pk):
    if User.objects.filter(pk=pk).exists():
        user = get_object_or_404(User, pk=pk)
        userPosts = Post.objects.filter(author=pk).order_by('-published_date')
        context = {
           'user': user,
            "userPosts": userPosts
        }
        return render(request, 'account/user_profile.html', context)
    else:
        return HttpResponse('Invalid ID')

def last_hour(self):
    time_treshold = timezone.now() - timedelta(hours=1)
    posts = serializers.serialize('json', Post.objects.filter(published_date__gte=time_treshold).order_by('-published_date'))
    return HttpResponse(posts, content_type='json')

def search(request):
    query = request.GET.get('q')
    control_text = str(Post.objects.values('title', 'text'))
    control_text.lower()
    counter = control_text.count(query)
    context = {
        'counter': counter,
        'query': query
    }
    return render(request, 'account/search.html', context)

def getIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
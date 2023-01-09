from django.shortcuts import render
from .forms import CreatePollForm
from .models import Poll
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='login')
def home(request):
    polls = Poll.objects.all()

    context = {
        'polls': polls
    }
    return render(request, 'poll/home.html', context)


def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = CreatePollForm()

    context = {'form': form}
    return render(request, 'poll/create.html', context)


def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    context = {
        'poll': poll
    }
    return render(request, 'poll/results.html', context)


def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll': poll
    }
    return render(request, 'poll/vote.html', context)


def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'poll/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            #login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'poll/login.html')
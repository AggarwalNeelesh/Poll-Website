from django.shortcuts import render, redirect
from .models import User, Question, Votes
from django.contrib.auth.models import User as UserAuth
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser


def login(request):
    # Super users are not common users
    if request.user.is_superuser:
        logout(request)

    # If user already logged in
    if request.user.is_authenticated:
        return redirect('/homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        userauth = authenticate(username=username, password=password)
        # Checking if user is registered or not
        if userauth is not None:
            # logging in the user
            loginUser(request, userauth)
            return redirect('/homepage')
        else:
            # No backend authenticated the credentials
            return render(request, 'polling/login.html')

    return render(request, 'polling/login.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('first_name') + " " + request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user_list = User.objects.filter(username=username)
        # When Username was already used
        if len(user_list) > 0:
            return render(request, 'polling/login.html', {"UserAlreadyRegistered": True})
        # Creating our custom User
        user = User(name=name, username=username, email=email, phone=phone, password=password, questions=0)
        user.save()
        # creating and saving the user of authentication
        userauth = UserAuth.objects.create_user(username=username, password=password)
        userauth.save()
        # redirecting user to logout page
        # If any user was previously logged in then it will be first logged out then login again.
        return redirect('/logout')
    else:
        return render(request, 'polling/register.html')


def logout(request):
    # logging out user
    logoutUser(request)
    return redirect('/login')


def homepage(request):
    # Super users are not common users
    if request.user.is_superuser:
        return redirect('/logout')

    # Checking if user is authenticated
    if request.user.is_authenticated:
        # By default Questions from all tags are displayed in homepage
        tag = 'All'
        if request.method == 'POST':
            # if a particular tag request has arrived
            tag = request.POST.get('tag') or 'All'

        if tag == 'All':
            allqueslist = Question.objects.all()
        else:
            allqueslist = Question.objects.filter(tag=tag)

        # Checking if user has already voted the question in question list
        u = User.objects.filter(username=request.user.username)[0]
        for i in allqueslist:
            votes_status = Votes.objects.filter(user_id=u.user_id, Q_id=i.Q_id)
            if len(votes_status) != 0:
                # Voted Already
                setattr(i, 'alreadyVoted', True)

        # Fetching List of all available tags to be displayed in homepage
        allTags = Question.objects.values('tag').distinct()
        return render(request, 'polling/homepage.html', {'quesList': allqueslist, 'username': request.user.username,
                                                         'allTags': allTags})
    else:
        return render(request, 'polling/login.html')


def profile(request):
    # Super users are not common users
    if request.user.is_superuser:
        return redirect('/logout')

    # Checking if user is authenticated
    if request.user.is_authenticated:
        u = User.objects.filter(username=request.user.username)[0]
        allqueslist = Question.objects.filter(user_id=u.user_id)

        for i in allqueslist:
            setattr(i, 'alreadyVoted', True)

        dic = {"name": u.name, "email": u.email, "phone": u.phone, "question": u.questions, 'quesList': allqueslist}
        return render(request, 'polling/profile.html', dic)
    else:
        return render(request, 'polling/login.html')


def createquestion(request):
    # Super users are not common users
    if request.user.is_superuser:
        return redirect('/logout')

    # Checking if user is authenticated
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Fetching user
            u = User.objects.filter(username=request.user.username)[0]
            # A user can create maximum of 5 questions
            if u.questions >= 5:
                return render(request, 'polling/createquestion.html', {"LimitExceeded": True})
            # Updating user details
            u.questions += 1
            u.save()
            ques = request.POST.get('ques')
            tag = request.POST.get('tag')
            opt1 = request.POST.get('opt1')
            opt2 = request.POST.get('opt2')
            opt3 = request.POST.get('opt3')
            opt4 = request.POST.get('opt4')
            question = Question(question=ques, op1=opt1, op2=opt2, op3=opt3, op4=opt4, user_id=u.user_id, tag=tag)
            question.save()
            return redirect('/homepage')
        return render(request, 'polling/createquestion.html')
    else:
        return render(request, 'polling/login.html')


def votes(request):
    # Super users are not common users
    if request.user.is_superuser:
        return redirect('/logout')

    # Checking if user is not authenticated
    if not request.user.is_authenticated:
        return render(request, 'polling/login.html')
    # Method to check that which user has voted for the question
    if request.method == 'POST':
        # Selected Option by User is op
        op = request.POST.get('op')
        qid = request.POST.get('qid')
        u = User.objects.filter(username=request.user.username)[0]
        ques = Question.objects.filter(Q_id=qid)[0]

        # Fetching If the user has voted this Question already
        votes_status = Votes.objects.filter(user_id=u.user_id, Q_id=qid)

        if len(votes_status) == 0:
            # Saving the vote of user
            vote = Votes(user_id=u.user_id, Q_id=qid)
            vote.save()
            print(op)
            # Updating votes on options of the question
            if op == "1":
                ques.vop1 += 1
            if op == "2":
                ques.vop2 += 1
            if op == "3":
                ques.vop3 += 1
            if op == "4":
                ques.vop4 += 1
            ques.save()

    return redirect('/homepage')


from django.shortcuts import render, redirect
from .models import User, Question, Votes
from django.contrib.auth.models import User as UserAuth
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser


def login(request):
    # If user already logged in
    if request.user.is_authenticated:
        return redirect('/homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        userauth = authenticate(username=username, password=password)
        if userauth is not None:
            # A backend authenticated the credentials
            loginUser(request, userauth)
            return redirect('/homepage')
        else:
            # No backend authenticated the credentials
            return render(request, 'polling/login.html')

    return render(request, 'polling/login.html')
    #
    #     user_list = User.objects.filter(username=username)
    #     # When User was not found
    #     if len(user_list) == 0:
    #         return render(request, 'polling/login.html', {"UserNotFound": True})
    #     if password != user_list[0].password:
    #         return render(request, 'polling/login.html', {"IncorrectPassword": True})
    #
    #     # Now we will go to home page
    #     global Uname
    #     Uname = username
    #
    #     Ulogin = True
    #     return redirect('/homepage')
    # else:
    #     return render(request, 'polling/login.html')


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
        # Creating User
        user = User(name=name, username=username, email=email, phone=phone, password=password, questions=0)
        user.save()

        userauth = UserAuth.objects.create_user(username=username, password=password)
        userauth.save()

        login(request)
        return render(request, 'polling/login.html')
    else:
        return render(request, 'polling/register.html')


def logout(request):
    logoutUser(request)
    return redirect('/login')


def homepage(request):
    Uname = request.user.username
    if request.user.is_authenticated:
        tag = 'All'

        if request.method == 'POST':
            tag = request.POST.get('tag') or 'All'

        if tag == 'All':
            allqueslist = Question.objects.all()
        else:
            allqueslist = Question.objects.filter(tag=tag)

        u = User.objects.filter(username=Uname)[0]
        for i in allqueslist:
            votes_status = Votes.objects.filter(user_id=u.user_id, Q_id=i.Q_id)
            if len(votes_status) != 0:
                # Voted Already
                setattr(i, 'alreadyVoted', True)
            # else:
            #     setattr(i, 'AlreadyVoted', False)

        # print(type(allqueslist[0].AlreadyVoted))
        allTags = Question.objects.values('tag').distinct()
        return render(request, 'polling/homepage.html', {'quesList': allqueslist, 'username': Uname,
                                                         'allTags': allTags})
    else:
        return render(request, 'polling/login.html')


def profile(request):
    Uname = request.user.username
    if request.user.is_authenticated:
        u = User.objects.filter(username=Uname)[0]
        print(Uname, u.name)
        allqueslist = Question.objects.filter(user_id=u.user_id)
        dic = {"name": u.name, "email": u.email, "phone": u.phone, "question": u.questions, 'quesList': allqueslist}
        return render(request, 'polling/profile.html', dic)
    else:
        return render(request, 'polling/login.html')


def createquestion(request):
    Uname = request.user.username
    if request.user.is_authenticated:
        if request.method == 'POST':
            us = User.objects.filter(username=Uname)
            print(Uname, us)
            if len(us) == 0:
                return render(request, 'polling/login.html')
            u = us[0]
            if u.questions >= 5:
                return render(request, 'polling/createquestion.html', {"LimitExceeded": True})
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
            allqueslist = Question.objects.all()
            return render(request, 'polling/homepage.html', {'quesList': allqueslist})
        return render(request, 'polling/createquestion.html')
    else:
        return render(request, 'polling/login.html')


def votes(request):
    if not request.user.is_authenticated:
        return render(request, 'polling/login.html')
    # Method to check that which user has voted for the question
    if request.method == 'POST':
        Uname = request.user.username
        # Selected Option by User is op
        op = request.POST.get('op')
        qid = request.POST.get('qid')
        u = User.objects.filter(username=Uname)[0]
        ques = Question.objects.filter(Q_id=qid)[0]

        # Fetching If the user has voted this Q already
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

from django.shortcuts import render
from .models import User, Question, Votes

Uname = ""


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_list = User.objects.filter(username=username)
        # When User was not found
        if len(user_list) == 0:
            return render(request, 'polling/login.html', {"UserNotFound": True})
        if password != user_list[0].password:
            return render(request, 'polling/login.html', {"IncorrectPassword": True})
        # Now we will go to home page
        global Uname
        Uname = username
        allqueslist = Question.objects.all()
        return render(request, 'polling/homepage.html', {'quesList': allqueslist, 'username': username})
    else:
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
        # Creating User
        user = User(name=name, username=username, email=email, phone=phone, password=password, questions=0)
        user.save()
        login(request)
        return render(request, 'polling/login.html')
    else:
        return render(request, 'polling/register.html')


def profile(request):
    global Uname
    u = User.objects.filter(username=Uname)[0]
    print(Uname, u.name)
    allqueslist = Question.objects.filter(user_id=u.user_id)
    dic = {"name": u.name, "email": u.email, "phone": u.phone, "question": u.questions, 'quesList': allqueslist}
    return render(request, 'polling/profile.html', dic)


def createquestion(request):
    global Uname
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
        opt1 = request.POST.get('opt1')
        opt2 = request.POST.get('opt2')
        opt3 = request.POST.get('opt3')
        opt4 = request.POST.get('opt4')
        question = Question(question=ques, op1=opt1, op2=opt2, op3=opt3, op4=opt4, user_id=u.user_id)
        question.save()
        allqueslist = Question.objects.all()
        return render(request, 'polling/homepage.html', {'quesList': allqueslist})
    return render(request, 'polling/createquestion.html')


def votes(request):
    # Method to check that which user has voted for the question
    allqueslist = Question.objects.all()
    if request.method == 'POST':
        global Uname
        # Selected Option by User is op
        op = request.POST.get('op')
        qid = request.POST.get('qid')
        us = User.objects.filter(username=Uname)
        ques = Question.objects.filter(Q_id=qid)[0]
        print(Uname, us)

        # If User is not logged in
        if len(us) == 0:
            return render(request, 'polling/login.html')
        u = us[0]
        # Fetching If the user has voted this Q already
        votes_status = Votes.objects.filter(user_id=u.user_id, Q_id=qid)

        already_voted = False
        # User has already voted
        if len(votes_status) == 1:
            already_voted = True
        else:
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

        dic = {'Voted': True, "AlreadyVoted": already_voted, 'quesList': allqueslist, "op1": ques.vop1, "op2": ques.vop2, "op3": ques.vop3, "op4": ques.vop4, "qid": qid}
        return render(request, 'polling/homepage.html', dic)

    return render(request, 'polling/homepage.html', {'quesList': allqueslist})

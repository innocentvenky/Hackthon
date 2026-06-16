from unicodedata import name

from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User ,Test,MCQ
from django.utils import timezone
import random

from django.db.models.functions import Random

from hackthon_app.models import User# Create your views here.
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        education = request.POST.get('Education')
        barnch = request.POST.get('Branch')
        college_name = request.POST.get('College')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        print(name, education, barnch, college_name, email, phone, date_of_birth, gender)
        try:
            User.objects.get(email=email)
            User.objects.get(phone=phone)
            messages.error(request, 'Email or phone number already exists.')
            return redirect('/register', {'messages': messages.get_messages(request)})
        except User.DoesNotExist:
            User.objects.create(name=name, education=education, email=email, phone=phone, date_of_birth=date_of_birth, gender=gender, branch=barnch, college_name=college_name)
            messages.success(request, 'User registered successfully.')
        return render(request, 'user\\success.html', {'name': name})
    return render(request, 'user\\register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.password == request.POST.get('password'):
                messages.success(request, 'Login successful.')
                if timezone.localtime(Test.objects.get(email=user).start_time)==None and timezone.localtime(Test.objects.get(email=user).end_time)==None:
                    messages.info(request, 'Test not scheduled yet.')
                    return render(request,'user\\success.html' ,{'messages': messages.get_messages(request)})
                elif timezone.localtime(Test.objects.get(email=user).start_time) <= timezone.localtime(timezone.now()) <= timezone.localtime(Test.objects.get(email=user).end_time):
                    request.session['user_email'] = user.email
                    return redirect('test_info/')
                elif timezone.localtime(timezone.now())> timezone.localtime(Test.objects.get(email=user).end_time):
                    messages.error(request, 'Expaired ')
                    return render(request,'user\\success.html' ,{'messages': messages.get_messages(request)})
                else:
                    messages.info(request,f'you test starts at {timezone.localtime(Test.objects.get(email=user).start_time).strftime("%d-%m-%Y %H:%M")}')
                    return redirect(request,'user\\success.html', {'messages': messages.get_messages(request)})

            else:
                messages.error(request, 'Invalid password.')
                return redirect('/', {'messages': messages.get_messages(request)})
        except User.DoesNotExist:
            messages.error(request, 'Invalid email id')
            return redirect('/', {'messages': messages.get_messages(request)})
    return render(request, 'user\\login.html')


def test_info(request):
    return render(request, 'hackthon_test\\test_info.html')


def mcq_test(request):
    obj=list(MCQ.objects.all())
    # mcqs=random.sample(obj,25)
    random.shuffle(obj)
   
    for mcq in obj:
        options=[
            mcq.option1,
            mcq.option2,
            mcq.option3,
            mcq.option4
        ]
        random.shuffle(options)
        mcq.shuffled_options=options
    if request.method=='POST':
        score=0
        for question in obj:
            select_answer=request.POST.get(f'question_{question.id}')
            if select_answer==question.answer:
                score +=1
        print(score)
    return render(request,'hackthon_test\\mcq_test.html',{'mcq':obj})
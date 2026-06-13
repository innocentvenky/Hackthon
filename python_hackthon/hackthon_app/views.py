from unicodedata import name

from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User ,Test
from django.utils import timezone
from hackthon_app.models import User# Create your views here.
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        education = request.POST.get('education')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        try:
            User.objects.get(email=email)
            User.objects.get(phone=phone)
            messages.error(request, 'Email or phone number already exists.')
            return redirect('register/', {'messages': messages.get_messages(request)})
        except User.DoesNotExist:
            User.objects.create(name=name, education=education, email=email, phone=phone, date_of_birth=date_of_birth)
            messages.success(request, 'User registered successfully.')
        return render(request, 'user\\success.html', {'name': name})
    return render(request, 'user\\register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            print(user)
            print(user.password)
            print(user.email)
            if user.password == request.POST.get('password'):
                messages.success(request, 'Login successful.')
                print(timezone.localtime(Test.objects.get(email=user).start_time))
                print(timezone.localtime(timezone.now()))
                if timezone.localtime(Test.objects.get(email=user).start_time) <= timezone.localtime(timezone.now()) <= timezone.localtime(Test.objects.get(email=user).end_time):
                    return redirect('test_info/')
                elif timezone.localtime(timezone.now())> timezone.localtime(Test.objects.get(email=user).end_time):
                    messages.error(request, 'Expaired ')
                    return redirect('/', {'messages': messages.get_messages(request)})
                else:
                    messages.info(request,f'you test starts at {timezone.localtime(Test.objects.get(email=user).start_time).strftime("%d-%m-%Y %H:%M")}')
                    return redirect('/', {'messages': messages.get_messages(request)})

            else:
                messages.error(request, 'Invalid password.')
                return redirect('/', {'messages': messages.get_messages(request)})
        except User.DoesNotExist:
            messages.error(request, 'Invalid email id')
            return redirect('/', {'messages': messages.get_messages(request)})
    return render(request, 'user\\login.html')


def test_info(request):
    return render(request, 'hackthon_test\\test_info.html')
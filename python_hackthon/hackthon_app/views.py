from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User ,Test,MCQ
from django.utils import timezone
import random
import subprocess
import ast 
import tempfile
import os
import random
from . models import CodingQuestion,TestCase

# Create your views here.
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
                try: 
                    if timezone.localtime(Test.objects.get(email=user).start_time) <= timezone.localtime(timezone.now()) <= timezone.localtime(Test.objects.get(email=user).end_time):
                        request.session['user_email'] = user.email
                        remaining_time=max(0,int((timezone.localtime(Test.objects.get(email=user).end_time)-timezone.now()).total_seconds()))
                        request.session['remaining_time'] = remaining_time
                        request.session.set_expiry(remaining_time)
                        print(request.session.get('user_email'))
                    
                        return redirect('test_info/')
                    elif timezone.localtime(timezone.now())> timezone.localtime(Test.objects.get(email=user).end_time):
                        messages.error(request, 'Expaired ')
                        return render(request,'user\\success.html' ,{'messages': messages.get_messages(request)})
                    else:
                        messages.info(request,f'you test starts at\t {timezone.localtime(Test.objects.get(email=user).start_time).strftime("%d-%m-%Y %H:%M")}')
                        return render(request,'user\\success.html', {'messages': messages.get_messages(request)})
                except Test.DoesNotExist:
                    messages.info(request, 'Test not scheduled yet.')
                    return render(request,'user\\success.html' ,{'messages': messages.get_messages(request)})
            else:
                messages.error(request, 'Invalid password.')
                return redirect('/', {'messages': messages.get_messages(request)})
        except User.DoesNotExist:
            messages.error(request, 'Invalid email id')
            return redirect('/', {'messages': messages.get_messages(request)})
    return render(request, 'user\\login.html')



def test_info(request):
    if request.session.get('user_email')==None:
        messages.error(request, 'Please login to access the test.')
        return redirect('/', {'messages': messages.get_messages(request)})
    else:
        if request.method=='POST':
            return redirect('/test_page')
        else:
            return render(request, 'hackathon_test\\test_info.html')



def test_page(request):
    email=request.session.get('user_email')
    user=User.objects.get(email=email)
    remaining_time=max(0,int((timezone.localtime(Test.objects.get(email=user).end_time)-timezone.now()).total_seconds()))
    request.session['remaining_time'] = remaining_time
    request.session.set_expiry(remaining_time)
    if request.session.get('user_email')!=None:
        return render(request, 'hackathon_test\\test_page.html',{'remaining_time':remaining_time})
    else:
        return redirect("login")


def mcq_test(request):
    email=request.session.get('user_email')
    user=User.objects.get(email=email)
    remaining_time=max(0,int((timezone.localtime(Test.objects.get(email=user).end_time)-timezone.now()).total_seconds()))
    request.session['remaining_time'] = remaining_time
    request.session.set_expiry(remaining_time)
    if user.mcq_test:
        if request.session.get('user_email')==None:
            messages.error(request, 'Please login to access the test.')
            return redirect('/', {'messages': messages.get_messages(request)})
        else:
            obj=list(MCQ.objects.all())
            random.shuffle(obj)
            mcqs=obj[:25]
            for mcq in mcqs:
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
                for question in mcqs:
                    select_answer=request.POST.get(f'question_{question.mcq_id}')
                    if select_answer==question.answer:
                        score +=1
                user.mcq_test=False
                user.mcq_marks=score
                user.total_marks=user.coding_marks+user.mcq_marks
                user.save()
                return redirect('/test_page')
        return render(request,'hackathon_test\\mcq_test.html',{'mcq':obj,'remaining_time':remaining_time})
    else:
        return redirect('/test_page')
    

def coding_questions(request):
    email=request.session.get('user_email')
    user=User.objects.get(email=email)
    remaining_time=max(0,int((timezone.localtime(Test.objects.get(email=user).end_time)-timezone.now()).total_seconds()))
    request.session['remaining_time'] = remaining_time
    request.session.set_expiry(remaining_time)
    if user.coding_test==True:
        questions=list(CodingQuestion.objects.all())
        random.shuffle(questions)
        coding_question=questions[:3]
        return render(request,'hackathon_test\coding_question.html',{'coding_question':coding_question, 'remaining_time':remaining_time})
    else:
        return redirect("/test_page")


def coding_test(request,id):
    email=request.session.get('user_email')
    print("email:",email)
    try:
        user=User.objects.get(email=email)
        remaining_time=max(0,int((timezone.localtime(Test.objects.get(email=user).end_time)-timezone.now()).total_seconds()))
        request.session['remaining_time'] = remaining_time
        request.session.set_expiry(remaining_time)
        if user.coding_test==True:
            total_mark=0
            total_tests=0
            total=0
            test_case_marks=3
            res={}
            task=CodingQuestion.objects.get(id=id)
            print(task.title)
            test_cases=TestCase.objects.filter(code=task.id)
            output=""
            code="def solve(*args):\n\t#write you code \n\tpass"
            if request.method=="POST":
                code=request.POST.get('code')
                temp_file = None
                submit=request.POST.get('action')
                try:
                    for i,testcase in enumerate(test_cases):
                        exceuted_code=code+"\n"
                        args=ast.literal_eval(testcase.test_input)
                        expected_output=str(ast.literal_eval(testcase.expected_output))
                        exceuted_code+=f'print(solve(*{args}))\n'
                        total_tests+=1
                        total+=test_case_marks
                        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix=".py", delete=False) as files:
                            files.write(exceuted_code)
                            files.flush()
                            result=subprocess.run(['python',files.name],capture_output=True,text=True,timeout=5)
                            output=result.stdout
                            if result.stderr:
                                output+=result.stderr
                            print(f"Test case {i+1}: {output.strip()}")
                            print(f"Expected output: {expected_output.strip()} output: {output.strip()}")
                            print(f"Match: {expected_output.strip() == output.strip()}")
                            if output.strip()==expected_output.strip():
                                res[f'Test case {i+1}'] = 'Passed'
                            elif output.strip()!=expected_output.strip():
                                res[f'Test case {i+1}'] = 'Failed'
                            print("value of :",submit)
                            print("reslut",submit=='submiting' or (request.POST.get("action")=='submiting'))
                            if submit=='submiting' or (request.POST.get("action")=='submiting'):
                                if output.strip()==expected_output.strip():
                                    res[f'Test case {i+1}'] = 'Passed'
                                    total_mark+=test_case_marks
                                    user.coding_test=False
                                    user.coding_marks=total_mark
                                    user.total_marks=user.coding_marks+user.mcq_marks
                    
                                elif output.strip()!=expected_output.strip():
                                    res[f'Test case {i+1}'] = 'Failed'
                                print(total_mark)
                                submit='submiting'
                    if submit=='submiting':
                        user.coding_test = False
                        user.coding_marks = total_mark
                        user.total_marks = user.coding_marks + user.mcq_marks
                        user.save()
                        return redirect('/test_page')

                except subprocess.TimeoutExpired:
                    output="Execution timed out."
                except Exception as e:  
                    output=str(e)
                finally:
                    if temp_file and os.path.exists(temp_file):
                        os.remove(temp_file)
                    user.save()
            return render(request,'hackathon_test\code_test.html', {"output": output,"code": code,"test":task,"test_cases":res,'remaining_time':remaining_time})
        else:
            return redirect('/test_page')
    except User.DoesNotExist:
        return redirect('/')

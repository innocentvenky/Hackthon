from django.db import models
import uuid
# Create your models here.
class User(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=100)
    edu=[('B.Tech','B.Tech'),('M.Tech','M.Tech'),('PhD','PhD')]
    education=models.CharField(max_length=100, choices=edu)
    l=[('CSE','CSE'),('ECE','ECE'),('EEE','EEE'),('CIVIL','CIVIL'),('MECHANICAL','MECHANICAL')]
    branch=models.CharField(max_length=100, choices=l)
    col=[("VISWAM","VISWAM"),('MITS','MITS'),('ADITYA','ADITYA'),('GVICS','GVICS')]
    college_name=models.CharField(max_length=100, choices=col)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15, unique=True)
    gen=[("Male","Male"),("Female","Female")]
    gender=models.CharField(max_length=10,choices=gen)
    created_at=models.DateTimeField(auto_now_add=True)
    date_of_birth=models.DateField()
    password=models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return self.email

class Test(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    start_time=models.DateTimeField(blank=True, null=True)
    end_time=models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"Test from {self.start_time} to {self.end_time}"

class MCQ(models.Model):
    question=models.TextField()
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    answer=models.CharField(max_length=200)
    def __str__(self):
        return self.question

class CodingTest(models.Model):
    question=models.TextField()
    sample_input=models.TextField()
    sample_output=models.TextField()
    def __str__(self):
        return self.question
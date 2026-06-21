from django.contrib import admin
from .models import User,Test,MCQ,Marks,CodingQuestion,TestCase
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'password','mcq_test','coding_test','phone', 'education','college_name','branch', 'date_of_birth', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('education','branch','college_name')
    ordering = ('-created_at',)
    def __str__(self):
        keywords = ['name', 'email', 'phone', 'education', 'college_name', 'branch', 'date_of_birth', 'created_at']
        return ', '.join(f"{keyword}: {getattr(self, keyword)}" for keyword in keywords)
admin.site.register(User, UserAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = ('get_user_name','get_user_branch', 'email', 'start_time', 'end_time')
    search_fields = ('email__name', 'email__email')
    list_filter = ('start_time', 'end_time')
    ordering = ('-start_time',)
    def __str__(self):
        keywords = ['id', 'email', 'start_time', 'end_time']
        return ', '.join(f"{keyword}: {getattr(self, keyword)}" for keyword in keywords)
    def get_user_name(self, obj):
        return obj.email.name
    get_user_name.short_description = 'User Name'
    def get_user_branch(self, obj):
        return obj.email.branch
    get_user_branch.short_description = 'User Branch'
admin.site.register(Test, TestAdmin)


class MCQAdmin(admin.ModelAdmin):
    list_display = ('mcq_id', 'question', 'option1', 'option2', 'option3', 'option4', 'answer')
    search_fields = ('question',)
    ordering = ('mcq_id',)
    def __str__(self):
        keywords = ['mcq_id', 'question', 'option1', 'option2', 'option3', 'option4', 'answer']
        return ', '.join(f"{keyword}: {getattr(self, keyword)}" for keyword in keywords)
admin.site.register(MCQ, MCQAdmin)


class MarksAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'mcq_marks', 'coding_marks', 'total_marks')
    search_fields = ('email__name', 'email__email')
    ordering = ('-total_marks',)
    def get_user_name(self, obj):
        return obj.email.name
    def __str__(self):
        keywords = ['id', 'email', 'mcq_marks', 'coding_marks', 'total_marks']
        return ', '.join(f"{keyword}: {getattr(self, keyword)}" for keyword in keywords)
admin.site.register(Marks, MarksAdmin)

class CodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'Input', 'Output')
admin.site.register(CodingQuestion,CodeAdmin)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('code', 'test_input', 'expected_output')
admin.site.register(TestCase,TestCaseAdmin)
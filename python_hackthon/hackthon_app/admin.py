from django.contrib import admin
from .models import User,Test,MCQ,CodingQuestion,TestCase

from django.http import HttpResponse
from openpyxl import Workbook

# Register your models here.

def export_users_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Users"

    # Header
    ws.append([

        "Name",
        "Email",
        "Phone",
        "Education",
        "College Name",
        "Branch",
        "Date Of Birth",
        "MCQ Test",
        "Coding Test",
        "MCQ Marks",
        "Coding Marks",
        "Total Marks",
    ])

    # Data
    for user in queryset:
        ws.append([
            user.name,
            user.email,
            str(user.phone),
            user.education,
            user.college_name,
            user.branch,
            str(user.date_of_birth),
            user.mcq_test,
            user.coding_test,
            user.mcq_marks,
            user.coding_marks,
            user.total_marks,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="users.xlsx"'

    wb.save(response)
    return response


export_users_excel.short_description = "Download selected users as Excel"


@admin.register(User)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'password','phone', 'education','college_name','branch', 'date_of_birth', 'created_at','mcq_test','coding_test','mcq_marks','coding_marks','total_marks')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('education','branch','college_name',)
    ordering = ('-created_at',)
    actions = [export_users_excel]


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

class CodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'Input', 'Output')
admin.site.register(CodingQuestion,CodeAdmin)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('code', 'test_input', 'expected_output')
admin.site.register(TestCase,TestCaseAdmin)
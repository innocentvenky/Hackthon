from django.contrib import admin
from .models import User,Test
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'phone', 'education','college_name','branch', 'date_of_birth', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('education','branch','college_name')
    ordering = ('-created_at',)
    def __str__(self):
        keywords = ['name', 'email', 'phone', 'education', 'college_name', 'branch', 'date_of_birth', 'created_at']
        return ', '.join(f"{keyword}: {getattr(self, keyword)}" for keyword in keywords)
admin.site.register(User, UserAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'start_time', 'end_time')
    search_fields = ('email__name', 'email__email')
    list_filter = ('start_time', 'end_time')
    ordering = ('-start_time',)
    def __str__(self):
        keywords = ['id', 'email', 'start_time', 'end_time']
        return ', '.join(f"{keyword}: {getattr(self, keyword)}" for keyword in keywords)
admin.site.register(Test, TestAdmin)
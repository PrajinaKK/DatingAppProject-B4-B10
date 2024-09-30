from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import User,Interest,Hobbies,Qualification,Location,Multiple_Image

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('username',)}
    list_display = ['username','slug','profile_pic']

admin.site.register(User,UsersAdmin)
admin.site.register(Interest)
admin.site.register(Hobbies)
admin.site.register(Qualification)
admin.site.register(Location)
admin.site.register(Multiple_Image)



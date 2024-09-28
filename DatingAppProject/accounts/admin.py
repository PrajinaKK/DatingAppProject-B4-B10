from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import User,Interest,Hobbies,Qualification,Location,Multiple_Image

# Register your models here.

admin.site.register(User)
admin.site.register(Interest)
admin.site.register(Hobbies)
admin.site.register(Qualification)
admin.site.register(Location)
admin.site.register(Multiple_Image)



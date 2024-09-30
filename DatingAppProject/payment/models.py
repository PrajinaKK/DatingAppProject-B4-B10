from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='group/', null=True, blank=True)
    members = models.ManyToManyField("accounts.User", related_name='group_members')
    admin = models.ManyToManyField("accounts.User", related_name='admin_groups')
    created = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    created_date = models.DateTimeField(null=True, blank=True)

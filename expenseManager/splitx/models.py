from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100, default='')

# Automatically create a UserProfile object when user object is created
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile, sender=User)

class Expense(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    created_by = models.ForeignKey(User)
    users = models.ManyToManyField(User, related_name='users')
    pub_date = models.DateTimeField('auto_now_add=True', default=timezone.now())

class Transaction(models.Model):
    paid_by = models.ForeignKey(User, related_name='paid_by')
    paid_to = models.ForeignKey(User, related_name='paid_to')
    expense_id = models.ForeignKey(Expense)
    amount = models.IntegerField()

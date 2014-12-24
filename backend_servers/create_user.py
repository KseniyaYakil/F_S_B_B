from django.contrib.auth.models import User
import os

User.objects.all().delete()
user = User.objects.create(username='tester', password='123', first_name='Professional Tester', email='tester@mail.ru')
print "created user: id {} username {} pass {}".format(user.pk, user.username, user.password)

user1 = User.objects.get(username='tester', password='123')
print "found user: id {} username {} pass {}".format(user1.pk, user1.username, user1.password)





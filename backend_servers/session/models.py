from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from .config import SessionConf

class SessionAuth(models.Model):
		cookie_token = models.CharField(max_length=1024, unique=True)
		creation_time = models.DateTimeField(auto_now=True)
		user = models.ForeignKey(User)

		def is_expired(self):
				time_now = datetime.now().replace(tzinfo=None)
				creation_time = self.creation_time.replace(tzinfo=None)

				print "DEB: live time {}".format((time_now - creation_time).total_seconds())
				print "DEB: config exp time {0}".format(SessionConf.exp_time)
				return (time_now - creation_time).total_seconds() >= SessionConf.exp_time

		def expires_in(self):
				return SessionConf.exp_time

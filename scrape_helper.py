import errno

try:
	import fcntl
except ImportError:
	pass

import logging
import os.path
import sys
import traceback

from django.conf import settings

# import boto.ec2.cloudwatch
# import boto.sns


PROJECT = os.path.basename(os.path.dirname(os.path.abspath(__file__))).split('-')[0]

# cloudwatch = boto.ec2.cloudwatch.connect_to_region('ap-southeast-1')
# sns = boto.sns.connect_to_region('ap-southeast-1')

class NotificationHandler(logging.Handler):
	def __init__(self, name='', level=logging.NOTSET):
		logging.Handler.__init__(self, level=level)
		self.name = name

	def emit(self, record):
		if not settings.DEBUG:
			loggername = '{0} {1}'.format(PROJECT, self.name) if self.name else PROJECT
			message = record.getMessage()
			# if 'Traceback' in message or \
			# 		'Error' in message or \
			# 		'Warning' in message or \
			# 		record.levelno >= logging.WARNING:
			# 	try:
			# 		sns.publish(
			# 			topic=settings.SNS_TOPIC_ARN,
			# 			message=u'{0}: {1}'.format(loggername, message),
			# 			subject=u'Notification: {0}'.format(loggername))
			# 	except Exception as e:
			# 		print ('Error sending log email.', e, traceback.format_exc())


def getlogger(name):
	logger = logging.getLogger(name)

	if not logger.handlers:
		# setup handlers
		formatter = logging.Formatter("%(asctime)s - %(message)s")
	
		log_to_file = True
		try:
			filehandler = logging.FileHandler(
				os.path.join(settings.BASE_DIR,
					'logs/{0}.log'.format(name.lower().replace(' ', '_'))))
			filehandler.setFormatter(formatter)
		except:
			log_to_file = False

		consolehandler = logging.StreamHandler()
		consolehandler.setFormatter(formatter)

		notificationhandler = NotificationHandler(name=name)
		notificationhandler.setFormatter(formatter)

		logger.setLevel(logging.DEBUG)
		if log_to_file: logger.addHandler(filehandler)
		logger.addHandler(consolehandler)
		logger.addHandler(notificationhandler)

	return logger


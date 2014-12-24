import urllib3
import json
from django.http import HttpResponse

class Agent(object):
		def send_req_to_service(self, url, method, fields=None, headers=None):
			fields = fields or {}
			headers = headers or {}
			http = urllib3.PoolManager()

			print("INF send {0} `{1}' with fields={2}, headers={3}".format(method, url, fields, headers))

			try:
				if method == 'PUT':
					response = http.urlopen(method, url, header=headers, body=json.dumps(fields))
				else:
					response = http.request(method, url, headers=headers, fields=fields)
				if response:
					print('INF recv status={0}, headers={1}, body={2}'.format(response.status, response.getheaders(), response.data))
				return response
			except Exception as ex:
				print('ERR: exception occured: {}'.format(ex))
				return None

class SessionAgent(object):
		session_url = 'http://127.0.0.1:8002/session'
		cookie_name = 'session_id'
		session_verify_method = 'verify/'
		session_auth_method = 'auth_user/'

		def __init__(self):
				self.proto_agent = Agent()

		def check_if_authorized(self, request):
				if self.cookie_name not in request.COOKIES:
						print "W: cookie is not setted"
						return 0

				cookie = request.COOKIES[self.cookie_name]
				print "DEB: cookie is {0}".format(cookie)

				if cookie is None:
						print "W: empty filed {0}".format(self.cookie_name)
						return 0

				response = self.send_req(uri=self.session_verify_method, method='GET', headers={'Cookie': cookie})

				if response is None:
						print "ERR: sending req to session FAILED"
						return -1
				if response.status != 200:
						print "INF: user is not authorized/cookie is expired. status = {0}".format(response.status)
						return 0

				session_ans = json.loads(response.data.decode('utf-8'))
				return 1 if session_ans['status'] == 'valid' else 0

		def send_req(self, uri, **kwards):
				print "DEB: {0}/{1}".format(self.session_url, uri)
				return self.proto_agent.send_req_to_service(url="{0}/{1}".format(self.session_url, uri), **kwards)

		def auth_user(self, username, password):
				print "DEB: ask for authorization. user `{}'".format(username)
				response = self.send_req(uri=self.session_auth_method, method='POST',
										fields={'user_login': username, 'user_pass': password})
				return response


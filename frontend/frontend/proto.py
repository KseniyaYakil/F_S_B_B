import urllib3
import json
from django.http import HttpResponse
import re

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

		cookie_key1 = 'cookie_token'
		cookie_key2 = 'user_id'

		session_verify_method = 'verify/'
		session_auth_method = 'auth_user/'
		session_logout_method = 'logout/'

		def __init__(self):
				self.proto_agent = Agent()

		def check_if_authorized(self, request):
				if self.cookie_key1 not in request.COOKIES or self.cookie_key2 not in request.COOKIES:
						print "W: cookies are not setted"
						return 0

				cookie_1 = request.COOKIES[self.cookie_key1]
				cookie_2 = request.COOKIES[self.cookie_key2]
				print "DEB: {} is {}".format(self.cookie_key1, cookie_1)
				print "DEB: {} is {}".format(self.cookie_key2, cookie_2)

				response = self.send_req(uri=self.session_verify_method, method='GET', headers={self.cookie_key1: cookie_1,
																								self.cookie_key2: cookie_2})

				if response is None:
						print "ERR: sending req to session FAILED"
						return -1
				if response.status != 200:
						print "INF: user is not authorized/cookie is expired. status = {0}".format(response.status)
						return 0

				session_ans = json.loads(response.data.decode('utf-8'))
				return 1 if session_ans['status'] == 'valid' else 0

		def logout_user(self, request):
				if self.cookie_key1 not in request.COOKIES or self.cookie_key2 not in request.COOKIES:
						print "W: cookies are not setted"
						return 0

				cookie_1 = request.COOKIES[self.cookie_key1]
				cookie_2 = request.COOKIES[self.cookie_key2]
				print "DEB: {} is {}".format(self.cookie_key1, cookie_1)
				print "DEB: {} is {}".format(self.cookie_key2, cookie_2)

				response = self.send_req(uri=self.session_logout_method, method='DELETE', headers={self.cookie_key1: cookie_1,
																								self.cookie_key2: cookie_2})
				if response is None:
						print "ERR: sending req to session FAILED"
						return -1
				if response.status != 200:
						print "INF: user is not authorized/cookie is expired. status = {0}".format(response.status)
						return 0

				session_ans = json.loads(response.data.decode('utf-8'))
				return 1 if session_ans['status'] == 'logged_out' else 0

		def send_req(self, uri, **kwards):
				print "DEB: {0}/{1}".format(self.session_url, uri)
				return self.proto_agent.send_req_to_service(url="{0}/{1}".format(self.session_url, uri), **kwards)

		def get_spec_cookie_val(self, key, cookie_str):
				pattern = ".*?({}=(?P<{}>[^\s;]*))".format(key, key)
				found_res = re.match(pattern, cookie_str)
				return found_res.group(key) if found_res and found_res.group(key) else None

		def parse_cookie_values(self, cookie_str):
				print "session cookies {}".format(cookie_str)

				found_val1 = self.get_spec_cookie_val(self.cookie_key1, cookie_str)
				found_val2 = self.get_spec_cookie_val(self.cookie_key2, cookie_str)

				if found_val1 and found_val2:
						print "DEB: found {} {}".format(self.cookie_key1, found_val1)
						print "DEB: found {} {}".format(self.cookie_key2, found_val2)

						res = dict()
						res[self.cookie_key1] = found_val1
						res[self.cookie_key2] = found_val2
						return res
				else:
						print "DEB: not found"
						return None

		def auth_user(self, username, password):
				print "DEB: ask for authorization. user `{}'".format(username)
				response = self.send_req(uri=self.session_auth_method, method='POST',
										fields={'user_login': username, 'user_pass': password})
				if response is None:
						raise Http404

				resp_data = json.loads(response.data.decode('utf-8'))
				print resp_data['status']

				if 'status' not in resp_data or resp_data['status'] != 'valid':
						return None

				return self.parse_cookie_values(response.getheaders()['Set-Cookie'])


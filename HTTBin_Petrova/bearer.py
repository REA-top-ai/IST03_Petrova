import requests
from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('user', 'pass')
session = requests.get('https://httpbin.org/basic-auth/user/pass', auth=basic)
print(f'{session.status_code} -- {session.json()}')
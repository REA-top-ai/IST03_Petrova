import requests
from requests.auth import HTTPDigestAuth


url = 'https://httpbin.org/digest-auth/auth/user/pass'
resp = requests.get(url, auth=HTTPDigestAuth('user', 'pass'))
print(resp.json())

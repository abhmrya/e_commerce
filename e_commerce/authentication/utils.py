# users/utils.py
import requests

def verify_recaptcha(token):
    secret_key = ''
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {'secret': secret_key, 'response': token}
    response = requests.post(url, data=data)
    result = response.json()
    return result.get('success', False)

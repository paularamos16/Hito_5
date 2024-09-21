import requests
import json
from django.contrib.auth.models import User
from main.models import UserProfile

def api_data(request):
    data = json.loads(requests.get('https://www.mindicador.cl/api').text)
    return {'indicators': data}

def type_user(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        return {'user_type': user_profile.user_type}
    else:
        return {'user_type': ''}
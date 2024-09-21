import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlyflans.settings')
application = get_wsgi_application()

from django.contrib.auth.models import User

print('Estos son los usuarios ingresados:\n')
users = User.objects.all()

for user in users:
    print(user.username)

usuario = input('\nIngrese el usuario para revisar permisos: ')

user = User.objects.get(username=f'{usuario}')
permissions = user.user_permissions.all()

if len(permissions) > 0:
    print(f'\nEl usuario "{usuario}", tiene los siguientes permisos:\n')
    for permission in permissions:
        print(permission.name)
else:
    print(f'\nAl usuario "{usuario}", no se le han asignado permisos\n')


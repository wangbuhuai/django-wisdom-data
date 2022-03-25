# Created by Dayu Wang (dwang@stchas.edu) on 2022-03-22

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-03-22


import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wisdom_data.settings')

application = get_asgi_application()

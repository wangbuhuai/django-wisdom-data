# Created by Dayu Wang (dwang@stchas.edu) on 2022-03-22

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-03-22


from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="index"),
    path("submit/", views.submit, name="submit")
]

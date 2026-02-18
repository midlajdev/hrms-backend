from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.homeView ),
    path('job/', views.JobView.as_view()),
    path('job/create/', views.JobCreateView.as_view())
]

from django.urls import path

from . import views

urlpatterns = [
    path('profiles/', views.CreateView.as_view()),
    path('profiles/<int:pk>/', views.ProfileUpdateDestroyRetrieveView.as_view()),
    path('experiences/', views.CreateExperienceView.as_view()),
    path('experiences/<int:pk>/', views.ExperienceUpdateDestroyView.as_view()),
]

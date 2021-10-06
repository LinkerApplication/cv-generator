from django.urls import path

from . import views

urlpatterns = [
    path('profiles/', views.CreateView.as_view({'post': 'create'})),
    path('profiles/<int:pk>/', views.ProfileUpdateDestroyRetrieveView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
        'patch': 'update'})),

    path('experiences/', views.CreateExperienceView.as_view({'post': 'create'})),
    path('experiences/<int:pk>/', views.ExperienceUpdateDestroyView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
        'patch': 'update'}), name='exp'),
]

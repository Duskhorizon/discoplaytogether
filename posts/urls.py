from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<int:event_id>', views.detail, name='detail'),
    path('participate/<int:event_id>', views.participate, name='participate'),
]

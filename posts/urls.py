from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<int:event_id>', views.detail, name='detail'),
    path('participate/<int:event_id>', views.participate, name='participate'),
    path('del_ev/<int:event_id>', views.del_ev, name='del_ev'),
    path('swap_not/<int:event_id>', views.swap_not, name='swap_not'),
]

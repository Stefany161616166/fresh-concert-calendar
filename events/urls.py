from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),

    # подробнее
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),

    # бронирование
    path('event/<int:event_id>/book/', views.booking_step_1, name='book_step_1'),
    path('event/<int:event_id>/seats/<int:booking_id>/', views.booking_step_2, name='book_step_2'),

    path('booking/success/', views.booking_success, name='booking_success'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('buses/', views.buses, name='buses'),
    path('buses/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
    path('prices/', views.priceCatalog, name='prices'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.submit_booking, name='booking'),
    path('booking/schedule/', views.booking_schedule, name='booking_schedule'),
    path('booking/schedule/2', views.booking_schedule2, name='booking_schedule2'),
    path('booking/schedule/3', views.booking_schedule3, name='booking_schedule3'),
    path('booking/schedule/4', views.booking_schedule4, name='booking_schedule4'),
    path('booking/completion', views.booking_completion, name='booking_completion'),
    path('booking/completed', views.booking_completed, name='booking_completed'),
    path('booking/failed', views.booking_failed, name='booking_failed')
]


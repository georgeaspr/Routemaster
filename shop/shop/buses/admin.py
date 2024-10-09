from django.contrib import admin
from .models import Bus
from .models import Schedule
from .models import Booking

# Register your models here.
class BusAdmin(admin.ModelAdmin):
  list_display = ("id", "city1", "city2", "price", )

admin.site.register(Bus, BusAdmin)

class ScheduleAdmin(admin.ModelAdmin):
  list_display = ("bus_id", "time1", "time2",)

admin.site.register(Schedule, ScheduleAdmin)


class BookingAdmin(admin.ModelAdmin):
  list_display = ("date", "hour", "firstName", "lastName", "route", "seat", "ticketType")

admin.site.register(Booking, BookingAdmin)
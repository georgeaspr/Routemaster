from django.db import models

class Bus(models.Model):
    city1 = models.CharField(max_length=255)
    city2 = models.CharField(max_length=255)
    price = models.FloatField(null = True)




class Schedule(models.Model):
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    time1 = models.TimeField()
    time2 = models.TimeField()

class Booking(models.Model):
    date = models.DateField()
    hour = models.CharField(max_length=255, null = True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    seat = models.IntegerField()
    ticketType = models.CharField(max_length=255)
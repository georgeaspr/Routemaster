from django.http import HttpResponse
from django.template import loader
from .models import Bus
from django.shortcuts import render, redirect
from .models import Schedule
from .models import Booking
import datetime
from django.db.models import Q

def buses(request):
    buses = Bus.objects.all().values()
    template = loader.get_template('buses.html')
    context = {
        'buses': buses,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    bus = Bus.objects.get(id=id)
    schedules = Schedule.objects.filter(bus_id=bus.id).order_by('time1')
    buses = Bus.objects.all()
    context = {
        'bus': bus,
        'schedules': schedules,
        'buses': buses,
    }
    return render(request, 'details.html', context)

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())
  
def testing(request):
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],   
  }
  return HttpResponse(template.render(context, request))

  
def schedule_table(request):
    schedules = Schedule.objects.all()
    return render(request, 'details.html', {'schedules': schedules})


def priceCatalog(request):
    # Get all Bus objects
    buses = Bus.objects.all()

    # Calculate the half prices
    half_prices = [bus.price / 2 for bus in buses]

    half25_prices = [bus.price - (bus.price * 0.25) for bus in buses]
    # Combine buses and halfPrices lists
    combined_data = zip(buses, half_prices, half25_prices)

    # Prepare the data to be sent to the template
    context = {
        'combined_data': combined_data
    }

    return render(request, 'priceCatalog.html',context)

def contact(request):
  template = loader.get_template('contact.html')
  return HttpResponse(template.render())



def submit_booking(request):
    if request.method == 'POST':
        date = request.POST.get('date_field')
        request.session['booking_date'] = date
        return redirect('booking_schedule')
    
    return render(request, 'booking_form.html')


def booking_schedule(request):
    date = request.session.get('booking_date')
    buses = Bus.objects.all().values()
    print(1)
    print(request.method)
    if request.method == 'POST':
        button_value = request.POST.get('button_value')
        print(button_value)
        print(1)
        if button_value == 'Athens':
            start = "Athens"
            x = "προορισμό"
            request.session['start_city'] = start
            request.session['x'] = x
            return redirect('booking_schedule2')
        elif button_value == 'Other':
            start = "--"
            x = "αφετηρία"
            request.session['start_city'] = start
            request.session['x'] = x
            return redirect('booking_schedule2')
    context = {
        'date': date,
        'buses': buses
    }

    return render(request, 'booking_schedule.html', context)


def booking_schedule2(request):
    date = request.session.get('booking_date')
    start = request.session.get('start_city')
    x = request.session.get('x')
    buses = Bus.objects.all().values()

    if request.method == 'POST':
        button_value = request.POST.get('button_value')
        print(button_value)
        if start == 'Athens':
            end = button_value
            print(end)
            request.session['start_city'] = start
            request.session['end_city'] = end
        else:
            start = button_value
            end = "Athens"
            request.session['start_city'] = start
            request.session['end_city'] = end
        return redirect('booking_schedule3')   
            
    context = {
        'date': date,
        'buses': buses,
        'start': start,
        'x' : x
    }
    return render(request, 'booking_schedule2.html', context)


def booking_schedule3(request):
    date = request.session.get('booking_date')
    start = request.session.get('start_city')
    end = request.session.get('end_city')
    if start == 'Athens':
        bus_ids = Bus.objects.filter(city1=end).values_list('id', flat=True)
        schedules = Schedule.objects.filter(bus_id__in=bus_ids).values_list('time1', flat=True)
    else:
        bus_ids = Bus.objects.filter(city1=start).values_list('id', flat=True)
        schedules = Schedule.objects.filter(bus_id__in=bus_ids).values_list('time2', flat=True)
        
    schedules_list = [datetime.datetime.strptime(str(schedule), "%H:%M:%S").time() for schedule in schedules]

    if request.method == 'POST':
        print(request.method)
        button_value = request.POST.get('button_value')
        time = button_value
        request.session['time'] = time
        return redirect('booking_schedule4') 

    context = {
        'date': date,
        'start': start,
        'end': end,
        'schedules': schedules_list
    }
    return render(request, 'booking_schedule3.html', context)

def booking_schedule4(request):
    date = request.session.get('booking_date')
    start = request.session.get('start_city')
    end = request.session.get('end_city')
    time = request.session.get('time')
    print(time)
    time = str(time)
    print(time)
    availableseats = [1, 2, 3, 4, 5] 
    booking = Booking.objects.all().values()

    findroute = Bus.objects.filter(Q(city1=start, city2=end) | Q(city1=end, city2=start))
   
    price = [bus.price for bus in findroute]
    half_price = [bus.price / 2 for bus in findroute]
    half25_prices = [bus.price - (bus.price * 0.25) for bus in findroute]

    print(price + half_price + half25_prices)

    route = start + ' - ' + end
    print(route)

    # Retrieve bookings with the same route and hour
    bookings = Booking.objects.filter(route=route, hour=time, date=date)

    # Extract the seat values from the bookings
    booked_seats = list(bookings.values_list('seat', flat=True))
    print(booked_seats)

    # Remove booked seats from availableseats
    availableseats = [seat for seat in availableseats if seat not in booked_seats]
    print(availableseats)

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        ticketType = request.POST.get('ticket')

        seatNo = request.POST.get('seat')

        request.session['route'] = route
        request.session['fname'] = fname
        request.session['lname'] = lname
        request.session['ticketType'] = ticketType
        request.session['seatNo'] = seatNo
        
        return redirect('booking_completion') 

    context = {
        'date': date,
        'start': start,
        'end': end,
        'time': time,
        'aseats': availableseats,
        'price': price,
        'halfpr': half_price,
        'half25': half25_prices
    }
    return render(request, 'booking_schedule4.html', context)



def booking_completion(request):
    date = request.session.get('booking_date')
    route = request.session.get('route')
    time = request.session.get('time')
    ticketType = request.session.get('ticketType')
    fname = request.session.get('fname')
    lname = request.session.get('lname')
    seatNo = request.session.get('seatNo')

    if request.method == 'POST':

        # Check if a booking with the same details exists
        booking_exists = Booking.objects.filter(
            date=date,
            hour=time,
            seat=seatNo,
        ).exists()

        if not booking_exists:
            new_booking = Booking(
                date=date,
                hour=time,
                firstName=fname,
                lastName=lname,
                route=route,
                seat=seatNo,
                ticketType=ticketType
            )
            new_booking.save()
            return redirect('booking_completed') 
        else:
            return redirect('booking_failed')

    context = {
        'date': date,
        'route': route,
        'time': time,
        'ticketType': ticketType,
        'fname': fname,
        'lname': lname,
        'seatNo': seatNo
    }

    return render(request, 'booking_completion.html', context)

def booking_completed(request):


     return render(request, 'booking_completed.html')


def booking_failed(request):

     return render(request, 'booking_failed.html')
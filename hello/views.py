from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Flight, Passenger

# Create your views here.
def index(request):
    context = {
        "flights":Flight.objects.all()

    }
    return render(request, "flights/index.html", context)


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight Does Not Exist!")

    context = {
        "flight" : flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)


def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message": "Passenger Does Not Exist!"})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "Flight Does Not Exist!"})
    except KeyError:
        return render(request, "flights/error.html", {"message": "No Selection!"})

    #Booking step
    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flights", args=(flight_id,)))

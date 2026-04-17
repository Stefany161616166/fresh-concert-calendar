from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Seat, Booking
from .forms import BookingForm


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

# ШАГ 1: форма с именем / email / телефоном
def booking_step_1(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event = event
            booking.save()
            # переходим на выбор места
            return redirect('book_step_2', event_id=event.id, booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'events/book_ticket.html', {
    'event': event,
    'form': form,
})


def _build_zone(event, zone, rows_count, order_desc=False):
    data = {}
    for row_number in range(1, rows_count + 1):
        qs = Seat.objects.filter(event=event, zone=zone, row=row_number)
        qs = qs.order_by("-number" if order_desc else "number")
        data[row_number] = list(qs)
    return data


# ШАГ 2: схема зала + выбор места
# views.py

def booking_step_2(request, event_id, booking_id):
    event = get_object_or_404(Event, id=event_id)
    booking = get_object_or_404(Booking, id=booking_id, event=event)

    error = None  # <-- чтобы переменная всегда существовала

    if request.method == "POST":
        seat_ids = request.POST.getlist("seats")  # getlist, а не get

        if not seat_ids:
            error = "Выберите хотя бы одно место."
        else:
            seats = Seat.objects.filter(event=event, id__in=seat_ids, booked=False)

            if seats.count() != len(seat_ids):
                error = "Одно или несколько мест уже заняты. Обновите страницу и выберите другие."
            else:
                seats.update(booked=True)

                cnt = len(seat_ids)
                if event.available_tickets >= cnt:
                    event.available_tickets -= cnt
                    event.save()

                return redirect("booking_success")

    ROWS_COUNT = 18
    left_by_row = _build_zone(event, "loge_left", ROWS_COUNT, order_desc=True)
    right_by_row = _build_zone(event, "loge_right", ROWS_COUNT, order_desc=False)

    rows = []
    for i in range(1, ROWS_COUNT + 1):
        rows.append({
            "num": i,
            "left": left_by_row.get(i, []),
            "right": right_by_row.get(i, []),
        })

    context = {
        "event": event,
        "booking": booking,
        "rows": rows,
        "error": error,
    }
    return render(request, "events/seat_map.html", context)

    

    ROWS_COUNT = 18
    left_by_row = _build_zone(event, "loge_left", ROWS_COUNT, order_desc=True)
    right_by_row = _build_zone(event, "loge_right", ROWS_COUNT, order_desc=False)

    rows = []
    for i in range(1, ROWS_COUNT + 1):
        rows.append({
            "num": i,
            "left": left_by_row.get(i, []),
            "right": right_by_row.get(i, []),
        })

    context = {
        "event": event,
        "booking": booking,
        "rows": rows,
        "error": error,
    }
    return render(request, "events/seat_map.html", context)

def booking_success(request):
    return render(request, 'events/success.html')

def home(request):
    return render(request, 'events/home.html')

def about_studio(request):
    return render(request, 'events/about.html')

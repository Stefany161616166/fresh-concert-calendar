from .seat_generator import generate_seats_for_event
from django.contrib import admin
from .models import Event, Booking, Seat

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'event_time', 'location', 'available_tickets')
    search_fields = ('title', 'location')
    list_filter = ('event_date',)

    actions = ['generate_seats']

    def generate_seats(self, request, queryset):
        for event in queryset:
            generate_seats_for_event(event)
        self.message_user(request, "Схема зала создана/обновлена для выбранных мероприятий.")

    generate_seats.short_description = "Создать/обновить схему зала"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'seat', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('event',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('event', 'zone', 'row', 'number', 'booked')
    list_filter = ('event', 'zone', 'booked')
    search_fields = ('event__title',)
    list_editable = ('booked',)
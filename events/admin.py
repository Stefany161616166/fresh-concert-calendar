from .seat_generator import generate_seats_for_event
from django.contrib import admin
from .models import Event, Booking, Seat


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'event_time', 'location', 'available_tickets')
    search_fields = ('title', 'location')

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title',
                'event_date',
                'event_time',
                'location',
                'description',
                'available_tickets',
                'image',
            )
        }),
        ('Первый блок участников', {
            'fields': (
                'performer_1_title',
                'performer_1_desc',
                'performer_1_image',
            )
        }),
        ('Второй блок участников', {
            'fields': (
                'performer_2_title',
                'performer_2_desc',
                'performer_2_image',
            )
        }),
        ('Гость программы', {
            'fields': (
                'guest_title',
                'guest_desc',
                'guest_image',
            )
        }),
        ('Программа концерта', {
            'fields': (
                'program',
            )
        }),
    )

    actions = ['generate_seats']

    def generate_seats(self, request, queryset):
        for event in queryset:
            generate_seats_for_event(event)
        self.message_user(request, 'Схема зала создана/обновлена для выбранных мероприятий.')

    generate_seats.short_description = "Создать/обновить схему зала"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'event', 'seat', 'created_at')
    list_filter = ('event', 'created_at')
    search_fields = ('name', 'phone', 'email')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('event', 'zone', 'row', 'number', 'booked')
    list_filter = ('event', 'zone', 'booked')
    search_fields = ('event__title',)
    list_editable = ('booked',)

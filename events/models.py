from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    available_tickets = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    performer_1_title = models.CharField('Название первого блока участников', max_length=200, blank=True)
    performer_1_desc = models.TextField('Описание первого блока участников', blank=True)
    performer_1_image = models.ImageField('Фото первого блока участников', upload_to='performers/', null=True, blank=True)

    performer_2_title = models.CharField('Название второго блока участников', max_length=200, blank=True)
    performer_2_desc = models.TextField('Описание второго блока участников', blank=True)
    performer_2_image = models.ImageField('Фото второго блока участников', upload_to='performers/', null=True, blank=True)

    guest_title = models.CharField('Название блока гостя', max_length=200, blank=True)
    guest_desc = models.TextField('Описание гостя программы', blank=True)
    guest_image = models.ImageField('Фото гостя программы', upload_to='guests/', null=True, blank=True)

    program = models.TextField('Концертная программа', blank=True)

    def __str__(self):
        return self.title


class Seat(models.Model):
    ZONE_CHOICES = [
        ('parter', 'Партер'),
        ('loge_left', 'Ложа левая'),
        ('loge_right', 'Ложа правая'),
        ('balcony', 'Балкон'),
    ]

    event = models.ForeignKey(Event, related_name='seats', on_delete=models.CASCADE)
    zone = models.CharField(max_length=20, choices=ZONE_CHOICES)
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'zone', 'row', 'number')
        ordering = ['zone', 'row', 'number']

    def __str__(self):
        return f'{self.get_zone_display()} — ряд {self.row}, место {self.number}'


class Booking(models.Model):
    event = models.ForeignKey(Event, related_name='bookings', on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat, related_name='bookings', blank=True)

    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Бронь {self.name} на "{self.event.title}"'

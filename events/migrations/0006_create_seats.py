from django.db import migrations


def create_seats(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    Seat = apps.get_model('events', 'Seat')

    event = Event.objects.get(id=1)

    Seat.objects.filter(event=event).delete()

    def create(zone, row, nums):
        for n in nums:
            Seat.objects.create(
                event=event,
                zone=zone,
                row=row,
                number=n,
                booked=False
            )

    for row in range(1, 19):
        if row == 1:
            left_nums = range(22, 12, -1)    # 22..13
            right_nums = range(11, 0, -1)    # 11..1
        elif row in (17, 18):
            left_nums = range(22, 11, -1)    # 22..12
            right_nums = range(11, 0, -1)    # 11..1
        else:
            left_nums = range(24, 12, -1)    # 24..13
            right_nums = range(12, 0, -1)    # 12..1

        create('loge_left', row, left_nums)
        create('loge_right', row, right_nums)


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_seat_options_remove_booking_tickets_and_more'),
    ]

    operations = [
        migrations.RunPython(create_seats),
    ]

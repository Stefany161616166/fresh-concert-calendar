from .models import Seat


def generate_seats_for_event(event):

    Seat.objects.filter(event=event).delete()

    def create(zone, row, nums):
        for n in nums:
            Seat.objects.create(
                event=event,
                zone=zone,
                row=row,
                number=n,
                booked=False,
            )

    for row in range(1, 19):
        if row == 1:
            left_nums = range(22, 12, -1)   # 22..13
            right_nums = range(11, 0, -1)   # 11..1
        elif row in (17, 18):
            left_nums = range(22, 11, -1)   # 22..12
            right_nums = range(11, 0, -1)   # 11..1
        else:
            left_nums = range(24, 12, -1)   # 24..13
            right_nums = range(12, 0, -1)   # 12..1

        create('loge_left', row, left_nums)
        create('loge_right', row, right_nums)

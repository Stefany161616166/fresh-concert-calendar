from django.core.management.base import BaseCommand
from events.models import Event, Seat


class Command(BaseCommand):
    help = "Создаёт места для схемы зала (18 рядов, левый/правый блок) для указанного event_id"

    def add_arguments(self, parser):
        parser.add_argument("event_id", type=int)

    def handle(self, *args, **options):
        event_id = options["event_id"]
        event = Event.objects.get(id=event_id)

        # удаляем старые места, чтобы не было дубликатов
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
            # ЛЕВО
            if row == 1:
                left_nums = list(range(22, 12, -1))  # 22..13
            elif row in (17, 18):
                left_nums = list(range(22, 11, -1))  # 22..12
            else:
                left_nums = list(range(24, 12, -1))  # 24..13

            # ПРАВО
            if row == 1:
                right_nums = list(range(11, 0, -1))  # 11..1
            elif row in (17, 18):
                right_nums = list(range(11, 0, -1))  # 11..1
            else:
                right_nums = list(range(12, 0, -1))  # 12..1

            create("loge_left", row, left_nums)
            create("loge_right", row, right_nums)

        self.stdout.write(self.style.SUCCESS(
            f"Готово! Создано мест: {Seat.objects.filter(event=event).count()} для event_id={event_id}"
        ))

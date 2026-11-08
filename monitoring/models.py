from django.db import models


class Device(models.Model):
    """Початкова модель ЛР16: без паспортів, міток і вимірювань."""
    name = models.CharField(max_length=80)
    serial = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"{self.name} ({self.serial})"

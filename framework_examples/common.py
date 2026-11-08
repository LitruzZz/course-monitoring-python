"""Спільні навчальні дані для двох HTTP-інтерфейсів."""
DEVICES = (
    {"id": 1, "serial": "T-01", "name": "Датчик температури"},
    {"id": 2, "serial": "T-02", "name": "Резервний датчик"},
)

def find_device(device_id: int) -> dict | None:
    """Повернути копію пристрою або None, не змінюючи набір даних."""
    for device in DEVICES:
        if device["id"] == device_id:
            return dict(device)
    return None

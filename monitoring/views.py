from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Device


@require_safe
@ensure_csrf_cookie
def index(request):
    """GET q лише фільтрує перелік; порожній q повертає всі пристрої."""
    query = request.GET.get("q", "").strip()
    devices = Device.objects.order_by("serial")
    if query:
        devices = devices.filter(name__icontains=query)
    return render(request, "monitoring/index.html",
                  {"devices": devices, "q": query})


@require_safe
def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, "monitoring/detail.html", {"device": device})

from django.contrib import admin
from .models import RfidScan

@admin.register(RfidScan)
class RfidScanAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "block", "date", "time")
    search_fields = ("uid", "name", "block")
    list_filter = ("block", "date")

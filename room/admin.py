from django.contrib import admin
from .models import Room, Seat

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'capacity')
    search_fields = ('name',)
    list_filter = ('capacity',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'row', 'seat_number', 'is_available')
    list_filter = ('is_available', 'room')
    search_fields = ('room__name', 'row')
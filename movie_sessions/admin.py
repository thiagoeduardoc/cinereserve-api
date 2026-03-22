from django.contrib import admin
from .models import Session, Seat, Ticket

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'room_name', 'start_time', 'room_capacity')
    search_fields = ('movie', 'start_time')
    list_filter = ('movie',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'row', 'number', 'status')
    list_filter = ('status', 'session__movie')
    search_fields = ('session__movie__title', 'row')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'seat', 'purchased_at')
    search_fields = ('user__username',)
    readonly_fields = ('purchased_at',)


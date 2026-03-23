from django.contrib import admin
from .models import Session, Ticket, Reservation

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'room', 'start_time')
    search_fields = ('movie__title', 'room__name', 'start_time')
    list_filter = ('movie', 'room')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'seat', 'session', 'reserved_at', 'expires_at', 'is_valid')
    search_fields = ('user__username', 'seat__row', 'session__movie__title')
    list_filter = ('session', 'reserved_at')
    readonly_fields = ('reserved_at', 'expires_at')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'seat', 'session', 'purchased_at')
    search_fields = ('user__username', 'seat__row', 'session__movie__title')
    readonly_fields = ('purchased_at',)


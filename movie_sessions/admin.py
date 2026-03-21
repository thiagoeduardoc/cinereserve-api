from django.contrib import admin
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'room_name', 'start_time', 'room_capacity')
    search_fields = ('movie', 'start_time')



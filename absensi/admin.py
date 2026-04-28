from django.contrib import admin
from .models import Attendance, LeaveRequest, UserProfile
from django.utils.html import format_html

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'status', 'location_link', 'thumbnail')
    list_filter = ('status', 'timestamp', 'user')
    search_fields = ('user__username',)

    def location_link(self, obj):
        return format_html('<a href="https://www.google.com/maps?q={},{}" target="_blank">Lihat Lokasi</a>', obj.latitude, obj.longitude)
    location_link.short_description = 'Lokasi'

    def thumbnail(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />', obj.foto.url)
        return "-"
    thumbnail.short_description = 'Foto'

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'tanggal_mulai', 'tanggal_selesai', 'status', 'created_at')
    list_filter = ('status',)
    actions = ['approve_leave', 'reject_leave']

    def approve_leave(self, request, queryset):
        queryset.update(status='Approved')
    approve_leave.short_description = "Setujui Cuti Terpilih"

    def reject_leave(self, request, queryset):
        queryset.update(status='Rejected')
    reject_leave.short_description = "Tolak Cuti Terpilih"

admin.site.register(UserProfile)

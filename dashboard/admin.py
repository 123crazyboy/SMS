from django.contrib import admin

from .models import (
    AttendanceRecord,
    DailyAttendance,
    Department,
    RecentActivity,
    RoomUsage,
    ScheduleItem,
    SchoolClass,
    Student,
    Subject,
    Teacher,
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "grade", "section", "guardian", "status")
    list_filter = ("grade", "section", "status", "has_scholarship", "needs_follow_up")
    search_fields = ("id", "name", "guardian")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subject", "department", "classes", "phone", "status")
    list_filter = ("department", "status")
    search_fields = ("id", "name", "subject", "phone")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department", "teachers", "classes", "weekly_hours", "status")
    list_filter = ("department", "status")
    search_fields = ("code", "name", "classes")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "coverage")
    search_fields = ("name",)


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "advisor", "room", "students", "schedule", "status")
    list_filter = ("status", "room")
    search_fields = ("code", "name", "advisor", "room")


@admin.register(RoomUsage)
class RoomUsageAdmin(admin.ModelAdmin):
    list_display = ("name", "use", "capacity")
    search_fields = ("name", "use")


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("school_class", "advisor", "present", "absent", "late", "submitted", "status", "date")
    list_filter = ("date", "status")
    search_fields = ("school_class", "advisor")


admin.site.register(DailyAttendance)
admin.site.register(ScheduleItem)
admin.site.register(RecentActivity)

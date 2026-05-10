from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

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


def format_number(value):
    return f"{value:,}"


def attendance_rate(records):
    totals = records.aggregate(present=Sum("present"), absent=Sum("absent"), late=Sum("late"))
    present = totals["present"] or 0
    absent = totals["absent"] or 0
    late = totals["late"] or 0
    total = present + absent + late
    if total == 0:
        return "0%"
    return f"{round((present / total) * 100)}%"


def stat(label, value, tone, change="Current academic year"):
    return {"label": label, "value": value, "tone": tone, "change": change}


def today_attendance():
    records = AttendanceRecord.objects.filter(date=timezone.localdate())
    if records.exists():
        return records
    return AttendanceRecord.objects.all()


def index(request):
    attendance_records = today_attendance()
    totals = attendance_records.aggregate(present=Sum("present"))
    present_today = totals["present"] or 0

    context = {
        "current_page": "dashboard",
        "stats": [
            stat("Students", format_number(Student.objects.count()), "blue", "Saved in database"),
            stat("Teachers", format_number(Teacher.objects.count()), "green", f"{Department.objects.count()} departments"),
            stat("Classes", format_number(SchoolClass.objects.count()), "amber", "Active schedule records"),
            stat("Attendance", attendance_rate(attendance_records), "rose", f"{format_number(present_today)} present today"),
        ],
        "quick_actions": [
            "Register student",
            "Add teacher",
            "Create class",
            "Record attendance",
        ],
        "schedule": [
            {
                "time": item.time.strftime("%H:%M"),
                "title": item.title,
                "meta": item.meta,
            }
            for item in ScheduleItem.objects.all()
        ],
        "recent_activity": list(RecentActivity.objects.values_list("description", flat=True)[:4]),
    }
    return render(request, "dashboard/index.html", context)


def students(request):
    now = timezone.now()
    new_admissions = Student.objects.filter(created_at__year=now.year, created_at__month=now.month).count()
    context = {
        "current_page": "students",
        "student_stats": [
            stat("Total students", format_number(Student.objects.count()), "blue"),
            stat("New admissions", format_number(new_admissions), "green"),
            stat("Scholarships", format_number(Student.objects.filter(has_scholarship=True).count()), "amber"),
            stat("Needs follow-up", format_number(Student.objects.filter(needs_follow_up=True).count()), "rose"),
        ],
        "students": Student.objects.all(),
    }
    return render(request, "dashboard/students.html", context)


def teachers(request):
    context = {
        "current_page": "teachers",
        "teacher_stats": [
            stat("Total teachers", format_number(Teacher.objects.count()), "blue"),
            stat("Class advisors", format_number(SchoolClass.objects.values("advisor").distinct().count()), "green"),
            stat("On leave", format_number(Teacher.objects.filter(status="Leave").count()), "amber"),
            stat("Vacancies", "0", "rose"),
        ],
        "departments": [
            {
                "name": department.name,
                "teachers": department.teachers.count(),
                "coverage": department.coverage,
            }
            for department in Department.objects.all()
        ],
        "teachers": Teacher.objects.select_related("department"),
    }
    return render(request, "dashboard/teacher.html", context)


def classes(request):
    context = {
        "current_page": "classes",
        "class_stats": [
            stat("Total classes", format_number(SchoolClass.objects.count()), "blue"),
            stat("Active sections", format_number(SchoolClass.objects.filter(status="Active").count()), "green"),
            stat("Rooms in use", format_number(RoomUsage.objects.count()), "amber"),
            stat("Capacity alerts", format_number(SchoolClass.objects.filter(students__gte=40).count()), "rose"),
        ],
        "classes": SchoolClass.objects.all(),
        "room_usage": RoomUsage.objects.all(),
    }
    return render(request, "dashboard/class.html", context)


def subjects(request):
    subjects_queryset = Subject.objects.select_related("department")

    context = {
        "current_page": "subjects",
        "subject_stats": [
            stat("Total subjects", format_number(subjects_queryset.count()), "blue"),
            stat("Assigned teachers", format_number(sum(subject.teachers for subject in subjects_queryset)), "green"),
            stat("Departments", format_number(Department.objects.count()), "amber"),
            stat("Pending setup", format_number(Subject.objects.filter(status="Pending").count()), "rose"),
        ],
        "subjects": subjects_queryset,
        "departments": [
            {
                "name": department.name,
                "subjects": department.subjects.count(),
                "coverage": department.coverage,
            }
            for department in Department.objects.all()
        ],
    }
    return render(request, "dashboard/subject.html", context)


def attendance(request):
    records = today_attendance()
    totals = records.aggregate(present=Sum("present"), absent=Sum("absent"), late=Sum("late"))
    present = totals["present"] or 0
    absent = totals["absent"] or 0
    late = totals["late"] or 0

    context = {
        "current_page": "attendance",
        "attendance_stats": [
            stat("Present today", format_number(present), "blue"),
            stat("Attendance rate", attendance_rate(records), "green"),
            stat("Late arrivals", format_number(late), "amber"),
            stat("Absent", format_number(absent), "rose"),
        ],
        "attendance_records": [
            {
                "class": record.school_class,
                "advisor": record.advisor,
                "present": record.present,
                "absent": record.absent,
                "late": record.late,
                "submitted": record.submitted.strftime("%H:%M"),
                "status": record.status,
            }
            for record in records
        ],
        "daily_breakdown": [
            {"day": day.day, "rate": f"{day.rate}%"}
            for day in DailyAttendance.objects.all()
        ],
    }
    return render(request, "dashboard/attendance.html", context)

import datetime

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


def seed_dashboard_data(apps, schema_editor):
    Student = apps.get_model("dashboard", "Student")
    Department = apps.get_model("dashboard", "Department")
    Teacher = apps.get_model("dashboard", "Teacher")
    SchoolClass = apps.get_model("dashboard", "SchoolClass")
    RoomUsage = apps.get_model("dashboard", "RoomUsage")
    AttendanceRecord = apps.get_model("dashboard", "AttendanceRecord")
    DailyAttendance = apps.get_model("dashboard", "DailyAttendance")
    ScheduleItem = apps.get_model("dashboard", "ScheduleItem")
    RecentActivity = apps.get_model("dashboard", "RecentActivity")

    students = [
        ("STU-1001", "Dara Sok", "Grade 12", "A", "Sokha Dara", "Active", True, False),
        ("STU-1002", "Lina Chan", "Grade 11", "B", "Chan Vireak", "Active", False, False),
        ("STU-1003", "Rithy Mao", "Grade 10", "A", "Mao Sopheak", "Pending", False, True),
        ("STU-1004", "Sophea Kim", "Grade 9", "C", "Kim Sovan", "Active", True, False),
        ("STU-1005", "Nita Heng", "Grade 8", "B", "Heng Pisey", "Inactive", False, False),
    ]
    for row in students:
        Student.objects.update_or_create(
            id=row[0],
            defaults={
                "name": row[1],
                "grade": row[2],
                "section": row[3],
                "guardian": row[4],
                "status": row[5],
                "has_scholarship": row[6],
                "needs_follow_up": row[7],
            },
        )

    departments = [
        ("Mathematics", "96%"),
        ("Science", "92%"),
        ("Languages", "98%"),
        ("Social Studies", "88%"),
    ]
    for name, coverage in departments:
        Department.objects.update_or_create(name=name, defaults={"coverage": coverage})

    teachers = [
        ("TCH-201", "Sok Vireak", "Mathematics", "10A, 11B", "+855 12 345 901", "Active", "Mathematics"),
        ("TCH-202", "Chan Sophea", "English", "8A, 9C", "+855 16 772 430", "Active", "Languages"),
        ("TCH-203", "Kim Ratanak", "Physics", "11A, 12A", "+855 15 220 118", "Leave", "Science"),
        ("TCH-204", "Heng Malis", "History", "7B, 8B", "+855 10 448 632", "Active", "Social Studies"),
        ("TCH-205", "Mao Sovan", "Biology", "9A, 10C", "+855 17 905 443", "Pending", "Science"),
    ]
    for row in teachers:
        Teacher.objects.update_or_create(
            id=row[0],
            defaults={
                "name": row[1],
                "subject": row[2],
                "classes": row[3],
                "phone": row[4],
                "status": row[5],
                "department": Department.objects.get(name=row[6]),
            },
        )

    classes = [
        ("CLS-10A", "Grade 10A", "Sok Vireak", "Room 204", 36, "Mon-Fri, 08:30", "Active"),
        ("CLS-11B", "Grade 11B", "Kim Ratanak", "Lab 2", 32, "Mon-Fri, 09:30", "Active"),
        ("CLS-09C", "Grade 9C", "Chan Sophea", "Room 118", 39, "Mon-Fri, 10:30", "Pending"),
        ("CLS-08B", "Grade 8B", "Heng Malis", "Room 112", 34, "Mon-Fri, 13:00", "Active"),
        ("CLS-12A", "Grade 12A", "Mao Sovan", "Room 301", 41, "Mon-Fri, 14:00", "Inactive"),
    ]
    for row in classes:
        SchoolClass.objects.update_or_create(
            code=row[0],
            defaults={
                "name": row[1],
                "advisor": row[2],
                "room": row[3],
                "students": row[4],
                "schedule": row[5],
                "status": row[6],
            },
        )

    rooms = [
        ("Room 204", "Math block", "36/40"),
        ("Lab 2", "Science block", "32/32"),
        ("Room 118", "Lower secondary", "39/40"),
        ("Room 301", "Senior classes", "41/42"),
    ]
    for name, use, capacity in rooms:
        RoomUsage.objects.update_or_create(name=name, defaults={"use": use, "capacity": capacity})

    records = [
        ("Grade 10A", "Sok Vireak", 34, 2, 1, datetime.time(8, 45), "Active"),
        ("Grade 11B", "Kim Ratanak", 30, 2, 3, datetime.time(9, 40), "Active"),
        ("Grade 9C", "Chan Sophea", 35, 4, 2, datetime.time(10, 38), "Pending"),
        ("Grade 8B", "Heng Malis", 33, 1, 0, datetime.time(13, 12), "Active"),
        ("Grade 12A", "Mao Sovan", 38, 3, 4, datetime.time(14, 10), "Pending"),
    ]
    for row in records:
        AttendanceRecord.objects.update_or_create(
            school_class=row[0],
            date=django.utils.timezone.localdate(),
            defaults={
                "advisor": row[1],
                "present": row[2],
                "absent": row[3],
                "late": row[4],
                "submitted": row[5],
                "status": row[6],
            },
        )

    for index, row in enumerate([("Mon", 96), ("Tue", 94), ("Wed", 92), ("Thu", 95), ("Fri", 93)], start=1):
        DailyAttendance.objects.update_or_create(day=row[0], defaults={"rate": row[1], "sort_order": index})

    schedule = [
        (datetime.time(8, 0), "Morning assembly", "Main hall"),
        (datetime.time(9, 30), "Grade 10 mathematics", "Room 204"),
        (datetime.time(11, 0), "Parent meeting", "Admin office"),
        (datetime.time(14, 0), "Science club", "Lab 2"),
    ]
    for index, row in enumerate(schedule, start=1):
        ScheduleItem.objects.update_or_create(
            title=row[1],
            defaults={"time": row[0], "meta": row[2], "sort_order": index},
        )

    activities = [
        "12 new student profiles created",
        "Grade 8 attendance submitted",
        "Teacher timetable updated",
        "Monthly fee report prepared",
    ]
    for description in activities:
        RecentActivity.objects.get_or_create(description=description)


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DailyAttendance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("day", models.CharField(max_length=10)),
                ("rate", models.PositiveIntegerField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                ("name", models.CharField(max_length=80, primary_key=True, serialize=False)),
                ("coverage", models.CharField(default="100%", max_length=10)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="RecentActivity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.CharField(max_length=160)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={"ordering": ["-created_at", "-id"], "verbose_name_plural": "recent activities"},
        ),
        migrations.CreateModel(
            name="RoomUsage",
            fields=[
                ("name", models.CharField(max_length=80, primary_key=True, serialize=False)),
                ("use", models.CharField(max_length=120)),
                ("capacity", models.CharField(max_length=20)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="ScheduleItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("time", models.TimeField()),
                ("title", models.CharField(max_length=120)),
                ("meta", models.CharField(max_length=120)),
                ("sort_order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["sort_order", "time"]},
        ),
        migrations.CreateModel(
            name="SchoolClass",
            fields=[
                ("code", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=80)),
                ("advisor", models.CharField(max_length=120)),
                ("room", models.CharField(max_length=80)),
                ("students", models.PositiveIntegerField(default=0)),
                ("schedule", models.CharField(max_length=120)),
                ("status", models.CharField(choices=[("Active", "Active"), ("Pending", "Pending"), ("Inactive", "Inactive")], default="Active", max_length=20)),
            ],
            options={"ordering": ["code"]},
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=120)),
                ("grade", models.CharField(max_length=30)),
                ("section", models.CharField(max_length=10)),
                ("guardian", models.CharField(max_length=120)),
                ("status", models.CharField(choices=[("Active", "Active"), ("Pending", "Pending"), ("Inactive", "Inactive")], default="Active", max_length=20)),
                ("has_scholarship", models.BooleanField(default=False)),
                ("needs_follow_up", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                ("id", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=120)),
                ("subject", models.CharField(max_length=80)),
                ("classes", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=30)),
                ("status", models.CharField(choices=[("Active", "Active"), ("Leave", "Leave"), ("Pending", "Pending")], default="Active", max_length=20)),
                ("department", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="teachers", to="dashboard.department")),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="AttendanceRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("school_class", models.CharField(max_length=80)),
                ("advisor", models.CharField(max_length=120)),
                ("present", models.PositiveIntegerField(default=0)),
                ("absent", models.PositiveIntegerField(default=0)),
                ("late", models.PositiveIntegerField(default=0)),
                ("submitted", models.TimeField()),
                ("status", models.CharField(choices=[("Active", "Active"), ("Pending", "Pending")], default="Pending", max_length=20)),
                ("date", models.DateField(default=django.utils.timezone.localdate)),
            ],
            options={"ordering": ["submitted", "school_class"]},
        ),
        migrations.RunPython(seed_dashboard_data, migrations.RunPython.noop),
    ]

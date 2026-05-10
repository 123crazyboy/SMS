from django.db import models
from django.utils import timezone


class Student(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Pending", "Pending"),
        ("Inactive", "Inactive"),
    ]

    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=120)
    grade = models.CharField(max_length=30)
    section = models.CharField(max_length=10)
    guardian = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")
    has_scholarship = models.BooleanField(default=False)
    needs_follow_up = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id} - {self.name}"


class Department(models.Model):
    name = models.CharField(max_length=80, primary_key=True)
    coverage = models.CharField(max_length=10, default="100%")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Teacher(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Leave", "Leave"),
        ("Pending", "Pending"),
    ]

    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=80)
    classes = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teachers",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id} - {self.name}"


class Subject(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Pending", "Pending"),
        ("Inactive", "Inactive"),
    ]

    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=80)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subjects",
    )
    teachers = models.PositiveIntegerField(default=0)
    classes = models.CharField(max_length=120, default="Not assigned")
    weekly_hours = models.PositiveIntegerField(default=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")

    class Meta:
        ordering = ["code"]

    @property
    def hours(self):
        return f"{self.weekly_hours} hrs"

    def __str__(self):
        return f"{self.code} - {self.name}"


class SchoolClass(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Pending", "Pending"),
        ("Inactive", "Inactive"),
    ]

    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=80)
    advisor = models.CharField(max_length=120)
    room = models.CharField(max_length=80)
    students = models.PositiveIntegerField(default=0)
    schedule = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.name


class RoomUsage(models.Model):
    name = models.CharField(max_length=80, primary_key=True)
    use = models.CharField(max_length=120)
    capacity = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Pending", "Pending"),
    ]

    school_class = models.CharField(max_length=80)
    advisor = models.CharField(max_length=120)
    present = models.PositiveIntegerField(default=0)
    absent = models.PositiveIntegerField(default=0)
    late = models.PositiveIntegerField(default=0)
    submitted = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    date = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["submitted", "school_class"]

    def __str__(self):
        return f"{self.school_class} - {self.date}"


class DailyAttendance(models.Model):
    day = models.CharField(max_length=10)
    rate = models.PositiveIntegerField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.day} {self.rate}%"


class ScheduleItem(models.Model):
    time = models.TimeField()
    title = models.CharField(max_length=120)
    meta = models.CharField(max_length=120)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "time"]

    def __str__(self):
        return self.title


class RecentActivity(models.Model):
    description = models.CharField(max_length=160)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at", "-id"]
        verbose_name_plural = "recent activities"

    def __str__(self):
        return self.description

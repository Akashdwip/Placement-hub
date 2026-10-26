
from django.conf import settings
from django.db import models


class Company(models.Model):
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="companies"
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    required_skills = models.TextField()

    minimum_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    location = models.CharField(max_length=100, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def skills_list(self):
        if not self.required_skills:
            return []
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]

    def __str__(self):
        return f"{self.title} - {self.company.name}"

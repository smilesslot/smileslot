from django.db import models
from bookings.models import Prescription
from Accounts.models import User
from Dashboard.models import ClinicReg
from slots.models import  StaffMember


class Education(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="educations"
    )
    college = models.CharField(max_length=300)
    degree = models.CharField(max_length=100)
    year_of_completion = models.IntegerField()

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Doctor Educations"

    def __str__(self) -> str:
        return (
            f"{self.user.get_full_name()} -> {self.college} -> {self.degree}"
        )


class Experience(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="experiences"
    )
    institution = models.CharField(max_length=300)
    from_year = models.IntegerField()
    to_year = models.IntegerField()
    working_here = models.BooleanField("Currently working here", default=False)
    designation = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Work & Experience"
        verbose_name_plural = "Works & Experiences"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} -> {self.institution}"



class Specialty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    doctors = models.ManyToManyField(User, related_name="specialties")

class Review(models.Model):
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_given"
    )
    doctor = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        related_name="reviews_received",
    )
    booking = models.OneToOneField(Prescription, on_delete=models.CASCADE
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["patient", "booking"]

    def __str__(self):
        return f"Review by {self.patient} for Dr. {self.doctor}"

    @property
    def rating_percent(self):
        return (self.rating / 5) * 100

import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    Http404,
    HttpResponsePermanentRedirect,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import (
    ListView,
    DetailView,
    View,
    CreateView,
)

from Clinic.models import Page
from slots.models import Service, Appointment, StaffMember
from django.views.generic.base import TemplateView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from django.db.models import Q
from django.db.models import Count
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from bookings.models import Prescription
from Dashboard.decorators import user_is_doctor
from doctors.forms import DoctorProfileUpdateForm,DoctorProfileExperienceForm, PrescriptionForm, DoctorUpdateForm
from doctors.models import Experience
from doctors.models.general import *
from doctors.serializers import (
    EducationSerializer,
    ExperienceSerializer,
    RegistrationNumberSerializer,
    SpecializationSerializer,

)
from mixins.custom_mixins import DoctorRequiredMixin
from utils.htmx import render_toast_message_for_api
from Accounts.models import User,Profile
from Dashboard.models import ClinicReg

days = {
    0: Sunday,
    1: Monday,
    2: Tuesday,
    3: Wednesday,
    4: Thursday,
    5: Friday,
    6: Saturday,
}


class DoctorDashboardView(DoctorRequiredMixin, TemplateView):
    template_name = "doctors/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        # Get appointment counts
        context["total_patients"] = (
            Booking.objects.filter(doctor=self.request.user)
            .values("patient")
            .distinct()
            .count()
        )

        context["today_patients"] = Booking.objects.filter(
            doctor=self.request.user, appointment_date=today
        ).count()

        context["total_appointments"] = Booking.objects.filter(
            doctor=self.request.user
        ).count()

        # Get upcoming appointments
        context["upcoming_appointments"] = (
            Appointment.objects.select_related("patient", "patient__profile")
            .filter(
                doctor_id=self.request.user,  
                date_of_appointment__gte=today,
                status__in=["pending", "confirmed"],
            )
            .order_by("date_of_appointment", "time_of_appointment")[:10]
        )

        # Get today's appointments
        context["today_appointments"] = (
            Booking.objects.select_related("patient", "patient__profile")
            .filter(doctor=self.request.user, appointment_date=today)
            .order_by("appointment_time")
        )

        return context

#perfect time format  human
def convert_to_24_hour_format(time_str):
    if time_str == "00:00 AM":
        time_str = "12:00 AM"
    return datetime.strptime(time_str, "%I:%M %p").time()



@login_required(login_url='/Accounts/login')
@user_is_doctor
def schedule_timings(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = request.POST
        for i in range(7):
            if data.get(f"day_{i}", None):
                start_times = data.getlist(f"start_time_{i}", default=[])
                end_times = data.getlist(f"end  _time_{i}", default=[])
                for index in range(len(start_times)):
                    start = convert_to_24_hour_format(start_times[index])
                    end = convert_to_24_hour_format(end_times[index])
                    time_range, time_created = TimeRange.objects.get_or_create(
                        start=start, end=end
                    )
                    day, created = days[i].objects.get_or_create(
                        user=request.user
                    )
                    ranges = day.time_range
                    if time_range.id not in list(
                        ranges.values_list("id", flat=True)
                    ):
                        day.time_range.add(time_range)

        return HttpResponsePermanentRedirect(
            reverse_lazy("doctors:schedule-timings")
        )

    return render(request, "doctors/schedule-timings.html")


def user_profile(request):
    user_view = request.user
    page = Page.objects.all()
    services = Specialization.objects.all()
    doctor = get_object_or_404(
            User, email=user_view, role=User.RoleChoices.DOCTOR
        )

    # Get appointments based on user type
    if user_view.is_staff:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(
            Q(email=user_view.email) |
            Q(mobile_number=user_view.mobile_number)
        ).order_by('-created_at')

    context = {
        'user_view': user_view,
        'page': page,
        'services': services,
        'appointments': appointments,
        'doctor':doctor,
    }

    if appointments.exists():
        messages.info(request, 'Your Appointment History')
        return render(request, 'dashboard/includes/profile.html', context)
    else:
        messages.info(request, 'No Appointment History Found')
        return render(request, 'user_profile/includes/profile.html', context)



class DoctorProfileUpdateView(DoctorRequiredMixin, generic.UpdateView):
    model = User
    template_name = "doctors/profile-settings.html"
    form_class = DoctorUpdateForm

    def get_object(self, queryset=None):
        return self.request.user



class DoctorUpdateView(DoctorRequiredMixin, generic.UpdateView):
    model = Profile
    template_name = "doctors/profile-settings.html"
    form_class = DoctorProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user



class DoctorProfileView(DetailView):
    context_object_name = "doctor"
    model = User
    slug_url_kwarg = "username"
    slug_field = "username"
    template_name = "doctors/profile.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        queryset = queryset.select_related("profile").prefetch_related(
            "educations",
            "experiences",
            "sunday__time_range",
            "monday__time_range",
            "tuesday__time_range",
            "wednesday__time_range",
            "thursday__time_range",
            "friday__time_range",
            "saturday__time_range",
        )

        try:
            obj = queryset.get(
                **{self.slug_field: slug, "role": User.RoleChoices.DOCTOR}
            )
        except User.DoesNotExist:
            raise Http404(f"No doctor found matching the username")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.object

        # Get current day name
        current_day = datetime.now().strftime("%A")

        # Prepare business hours
        business_hours = {
            "Sunday": (
                doctor.sunday.time_range.all()
                if hasattr(doctor, "sunday")
                else []
            ),
            "Monday": (
                doctor.monday.time_range.all()
                if hasattr(doctor, "monday")
                else []
            ),
            "Tuesday": (
                doctor.tuesday.time_range.all()
                if hasattr(doctor, "tuesday")
                else []
            ),
            "Wednesday": (
                doctor.wednesday.time_range.all()
                if hasattr(doctor, "wednesday")
                else []
            ),
            "Thursday": (
                doctor.thursday.time_range.all()
                if hasattr(doctor, "thursday")
                else []
            ),
            "Friday": (
                doctor.friday.time_range.all()
                if hasattr(doctor, "friday")
                else []
            ),
            "Saturday": (
                doctor.saturday.time_range.all()
                if hasattr(doctor, "saturday")
                else []
            ),
        }

        context.update(
            {
                "current_day": current_day,
                "business_hours": business_hours,
                #"reviews": doctor.reviews_received.select_related(
                 #    "patient", "patient__profile"
                 #).order_by("-created_at"),
            }
        )

        return context


class UpdateEducationAPIView(DoctorRequiredMixin, UpdateAPIView):
    queryset = Experience.objects.all()
    serializer_class = EducationSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        data = request.POST
        ids = data.getlist("id", default=[])
        degrees = data.getlist("degree", default=[])
        colleges = data.getlist("college", default=[])
        years = data.getlist("year_of_completion", default=[])
        for i in range(len(degrees)):
            try:
                instance = self.request.user.educations.get(id=ids[i])
                degree = degrees[i]
                college = colleges[i]
                year_of_completion = years[i]
                serializer = self.get_serializer(
                    instance,
                    data={
                        "degree": degree,
                        "college": college,
                        "year_of_completion": year_of_completion,
                    },
                    partial=True,
                )
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
            except:
                degree = degrees[i]
                college = colleges[i]
                year_of_completion = years[i]
                serializer = self.get_serializer(
                    data={
                        "degree": degree,
                        "college": college,
                        "year_of_completion": year_of_completion,
                    }
                )
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

        response = Response({"success": True})
        response.headers["HX-Trigger"] = json.dumps(
            {
                "show-toast": {
                    "level": "success",
                    "title": "Education",
                    "message": "Successfully updated",
                }
            }
        )
        return response


class UpdateExperienceAPIView(DoctorRequiredMixin, UpdateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        data = request.POST
        ids = data.getlist("id", default=[])
        institutions = data.getlist("institution", default=[])
        from_years = data.getlist("from_year", default=[])
        to_years = data.getlist("to_year", default=[])
        designations = data.getlist("designation", default=[])

        for i in range(len(institutions)):
            try:
                instance = self.request.user.educations.get(id=ids[i])
                institution = institutions[i]
                from_year = from_years[i]
                to_year = to_years[i]
                designation = designations[i]
                serializer = self.get_serializer(
                    instance,
                    data={
                        "institution": institution,
                        "from_year": from_year,
                        "to_year": to_year,
                        "designation": designation,
                    },
                    partial=True,
                )
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
            except:
                institution = institutions[i]
                from_year = from_years[i]
                to_year = to_years[i]
                designation = designations[i]
                serializer = self.get_serializer(
                    data={
                        "institution": institution,
                        "from_year": from_year,
                        "to_year": to_year,
                        "designation": designation,
                    }
                )
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

        return render_toast_message_for_api(
            "Experience", "Updated successfully", "success"
        )


class UpdateRegistrationNumberAPIView(DoctorRequiredMixin, UpdateAPIView):
    serializer_class = RegistrationNumberSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        data = request.POST
        serializer = self.get_serializer(instance=request.user, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return render_toast_message_for_api(
            "BM&DC number", "Updated successfully", "success"
        )


class UpdateSpecializationAPIView(DoctorRequiredMixin, UpdateAPIView):
    serializer_class = SpecializationSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.POST
        specialist = data.get("specialist")
        instance.profile.specialization = specialist
        instance.profile.save()

        return render_toast_message_for_api(
            "Specialization", "Updated successfully", "success"
        )



@login_required(login_url='/Accounts/login')
class DoctorsListView(ListView):
    model = User
    context_object_name = "doctors"
    template_name = "doctors/list.html"
    paginate_by = 2

    def get_queryset(self):
        queryset = self.model.objects.filter(
            role=User.RoleChoices.DOCTOR, is_stuff=True, is_active=True
        ).select_related("profile")

        # Handle search query
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(profile__specialization__icontains=search_query)
                | Q(profile__city__icontains=search_query)
            )

        # Handle gender filter
        gender = self.request.GET.getlist("gender")
        if gender:
            queryset = queryset.filter(profile__gender__in=gender)

        # Handle specialization filter
        specializations = self.request.GET.getlist("specialization")
        if specializations:
            queryset = queryset.filter(
                profile__specialization__in=specializations
            )

        # Handle sorting
        sort_by = self.request.GET.get("sort")
        if sort_by:
            if sort_by == "price_low":
                queryset = queryset.order_by("profile__price_per_consultation")
            elif sort_by == "price_high":
                queryset = queryset.order_by(
                    "-profile__price_per_consultation"
                )
            elif sort_by == "rating":
                queryset = queryset.order_by("-rating")
            elif sort_by == "experience":
                queryset = queryset.order_by("-profile__experience")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add search query to context
        context["search_query"] = self.request.GET.get("q")

        # Add unique specializations to context
        specializations = (
            User.objects.filter(role=User.RoleChoices.DOCTOR, is_active=True)
            # .exclude(profile__specialization__is__null=True)
            .values_list("specialization", flat=True)
            .distinct()
        )

        context["specializations"] = sorted(
            list(filter(None, specializations))
        )

        return context


class AppointmentListView(ListView):
    model = Prescription
    context_object_name = "appointments"
    template_name = "doctors/appointments.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            self.model.objects.select_related(
                "doctor", "doctor__profile", "patient", "patient__profile"
            )
            .filter(doctor=self.request.user)
            .order_by("-appointment_date", "-appointment_time")
        )


class AppointmentDetailView(DoctorRequiredMixin, DetailView):
    model = Prescription
    template_name = "dashboard/includes/patient_appointment_details.html"
    context_object_name = "appointment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object.patient

        # Get patient's appointment history with this doctor
        context["patient_history"] = (
            Prescription.objects.select_related("doctor", "doctor__profile")
            .filter(
                doctor=self.request.user,
                patient=patient,
                appointment_date__lt=self.object.appointment_date,
            )
            .order_by("-appointment_date", "-appointment_time")
        )
        appointment_ok = Appointment.objects.filter(appointee=patient)

        # Get total visits count
        context["total_visits"] = Booking.objects.filter(
            doctor=self.request.user, patient=patient,
        ).count()

        return context


class AppointmentActionView(DoctorRequiredMixin, View):
    def post(self, request, pk, action):
        appointment = get_object_or_404(
            Prescriptipn,
            pk=pk,
            doctor=request.user,
            status__in=["pending", "confirmed"],
        )

        if action == "accept":
            appointment.status = "confirmed"
            messages.success(request, "Appointment confirmed successfully")
        elif action == "cancel":
            appointment.status = "cancelled"
            messages.success(request, "Appointment cancelled successfully")
        elif action == "completed":
            appointment.status = "completed"
            messages.success(
                request, "Appointment marked as completed successfully"
            )

        appointment.save()
        return redirect("doctors:dashboard")

class MyPatientsView(DoctorRequiredMixin, ListView):
    template_name = "doctors/my-patients.html"
    context_object_name = "patients"

    def get_queryset(self):
        # Get unique patients who have appointments with this doctor
        return (
            ClinicStaff.objects.filter(
                appointments__doctor=self.request.user, role="patient"
            )
            .distinct()
            .select_related("profile")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get appointment counts for each patient
        patient_stats = {}
        for patient in context["patients"]:
            stats = Booking.objects.filter(
                doctor=self.request.user, patient=patient
            ).aggregate(
                total_appointments=Count("id"),
                completed_appointments=Count(
                    "id", filter=Q(status="completed")
                ),
            )
            patient_stats[patient.id] = stats
        context["patient_stats"] = patient_stats
        return context


class AppointmentHistoryView(DoctorRequiredMixin, ListView):
    model = Prescription
    template_name = "doctors/add_prescription.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return (
            self.model.objects.select_related("patient", "patient__profile")
            .filter(
                doctor=self.request.user, patient_id=self.kwargs["patient_id"]
            )
            .order_by("-appointment_date", "-appointment_time")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient"] = get_object_or_404(
            User.objects.select_related("profile"),
            id=self.kwargs["patient_id"],
            role="patient",
        )
        return context



class PrescriptionCreateView(DoctorRequiredMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "dashboard/includes/doctor_appointment_list_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.kwargs.get("booking_id")
        context["booking"] = get_object_or_404(
            Booking, id=booking_id, doctor=self.request.user
        )
        return context

    def form_valid(self, form):
        booking_id = self.kwargs.get("booking_id")
        booking = get_object_or_404(
            Prescription, id=booking_id, doctor=self.request.user
        )

        if Appointment.status != "completed":
            messages.error(
                self.request,
                "Can only add prescription for completed appointments",
            )
            return redirect("dashboard:patient_appointment_details", pk=booking_id)

        form.instance.booking = booking
        form.instance.doctor = self.request.user
        form.instance.patient = booking.patient
        messages.success(self.request, "Prescription added successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:patient_appointment_details",
            kwargs={"pk": self.kwargs["booking_id"]},
        )


class PrescriptionDetailView(DoctorRequiredMixin, DetailView):
    model = Prescription
    template_name = "doctors/prescription_detail.html"
    context_object_name = "prescription"

    def get_queryset(self):
        # Only allow doctors to view prescriptions they wrote
        return Prescription.objects.filter(
            doctor=self.request.user
        ).select_related(
            "appointment_ok",
            "doctor",
            "patient",
        )

from slots.models import Appointment, Service, StaffMember, AppointmentRequest
import random
from datetime import date, timedelta,datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Clinic.models import Page
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from Dashboard.models import ClinicReg
from Accounts.models import User
from django.core.mail import send_mail
from .utils import send_sms,send_sms_via_email
from django.template.loader import render_to_string
import africastalking
from datetime import datetime
from bookings.models import Prescription
from django.http import HttpResponse
from django.views.generic import UpdateView, DetailView, View, CreateView
import string
import segno
from slots.models import *
from slots.utils.date_time import convert_str_to_time,get_ar_end_time,convert_str_to_date

def generate_service_id():
    alphanumeric = string.digits
    return ''.join(random.choices(alphanumeric, k=6))


@login_required(login_url='/Accounts/login')
def User_Search_Appointments(request):
    page = Page.objects.all()
    MemberUser = request.user

    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=MemberUser) | Appointment.objects.filter(appointment_number__icontains=query)
            if patient:
                Appointment_History = Appointment.objects.filter(
                    email__icontains=MemberUser
                    ) | Appointment.objects.filter(
                    appointment_number__icontains=query) & Appointment.objects.filter(appointee=MemberUser)
                messages.info(request, "Search against " + query)
                context = {'patient': Appointment_History, 'query': query, 'page': page}
                return render(request, 'appointment/includes/view_appointment.html', context)
            else:
                messages.info(request, "No records found matching " + query)
                context = {'page': page}
                return render(request, 'appointment/search-appointment.html', context)

        # If the request method is not GET
        return render(request, 'appointment/search-appointment.html')



@login_required(login_url='/Accounts/login')
def user_profile_history_appointment(request):
    user_view = request.user
    page = Page.objects.all()
    Services = Specialization.objects.all()
    context = {'services': Services, 'page': page}
    Appointment_History = Appointment.objects.filter(email__icontains=user_view) | Appointment.objects.filter(
        mobile_number__icontains=user_view)
    if Appointment_History:
        # Filter records where fullname or Appointment Number contains the query
        Appointee = Appointment_History
        messages.info(request, 'Your Appointment History Exists')
        context = {'Appointee': Appointee, 'user_view': user_view, 'page': page, 'services': Services, }
        return render(request, 'user_profile/includes/profile.html', context)
    return render(request, 'user_profile/user_profile.html', context)


def View_Appointment_Details(request, id):
    page = Page.objects.all()
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails,
               'page': page

               }

    return render(request, 'appointment/includes/user_appointment-details.html', context)


@login_required(login_url='/Accounts/login')
def View_Appointment(request):
    try:
        doctor_reg = DoctorReg.objects.get(admin=request.user)
        view_appointment = Appointment.objects.filter(doctor_id=doctor_reg)

        # Pagination
        paginator = Paginator(view_appointment, 5)  # Show 10 appointments per page
        page = request.GET.get('page')
        try:
            view_appointment = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            view_appointment = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            view_appointment = paginator.page(paginator.num_pages)

        context = {'view_appointment': view_appointment}
    except Exception as e:
        # Handle exceptions, such as database errors, gracefully
        context = {'error_message': str(e)}

    return render(request, 'appointment/includes/view_appointment.html', context)


def AppointmentHistoryList(request, id):
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails

               }
    return render(request, 'dashboard/includes/doctor_appointment_list_details.html', context)



def create_appointment(request):
    clinic_view = (ClinicReg.objects
        .select_related("member"))
        #.filter(role="doctor")
        #.filter(is_superuser=False))
    worry = Service.objects.all()
    page = Page.objects.all()

    if request.method == "POST":
#        appointment_number = random.randint(100000000, 999999999)
        appointment_number =  generate_service_id()
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        date_of_appointment = request.POST.get('date_of_appointment')
        time_of_appointment = request.POST.get('time_of_appointment')
        clinic = request.POST.get('clinic_id')
        service = request.POST.get('worry_need')
        additional_msg = request.POST.get('additional_msg')

        # Retrieve the DoctorReg and Specialization instances
        clinic_instance = ClinicReg.objects.get(slug=clinic)
        service_instance = Service.objects.get(id=service)
        start = time_of_appointment

        # Create appointment
        appointment_details = AppointmentRequest.objects.create(
            appointment_number=appointment_number,
            status="Pending",
            fullname=full_name,
            email=email,
            mobile_number=mobile_number,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            service=service_instance,
            additional_msg=additional_msg,
            clinic=clinic_instance,
            start_time=convert_str_to_time(time_of_appointment),
            date=convert_str_to_date(date_of_appointment),
            end_time=get_ar_end_time(start,service_instance.duration)
            #end_time=service_instance.duration + start
        )

        # Send SMS and email notifications
        try:
            subject = "Appointment Confirmation"
            message = (
                f"Dear {full_name},\n\n"
                f"{mobile_number},\n\n"
                f"Thank you for scheduling an appointment with us.\n\n"
                f"Appointment Details:\n"
                f"Appointment Number: {appointment_number}\n"
                f"Date: {date_of_appointment}\n"
                f"Time: {time_of_appointment}\n"
                f"Doctor: {clinic}\n"
                f"Duration: {service_instance.get_duration()}\n"
                f"Concern: {service}\n\n"
                f"We look forward to serving you.\n\n"
                f"Best regards,\n"
                f"SmileSlot"
            )
            send_mail(
                subject,
                message,
                '{email}',  # Replace with your clinic's email
                [email, 'mboatechnologies@gmail.com'],  # Recipients
                fail_silently=False,
            )

            sms_message = (
                f"Hello {full_name},\n"
                f"Your appointment has been confirmed.\n"
                f"Appointment Number: {appointment_number}\n"
                f"Date: {date_of_appointment}\n"
                f"Time: {time_of_appointment}\n"
                f"Doctor: {clinic}\n"
                f"Concern: {service}\n"
                f"Thank you for choosing us!"
            )
            send_sms_via_email(mobile_number, sms_message)  # Assuming send_sms is implemented correctly


            messages.success(request, "Appointment confirmed. Notifications sent successfully.")
        except Exception as e:
            messages.error(request, f"Failed to send notifications: {str(e)}")

        return render(request,'account/includes/appointment_success.html', {'appointment_details': appointment_details})  # Redirect to a success page

    context = {'clinic': clinic_view, 'worry': worry, 'page': page}
    return render(request, 'user_profile/includes/appointment_form.html', context)




@login_required
def update_user_appointment(appointment_number, request, self):
     user = request.user
     clinic_reg, = ClinicReg.objects.get(member=user)
     Appointment, _ = Appointment.objects.get_or_create(appointment_number=self.appointment_number)|Appointment.objects.get_or_create(clinic=clinic_reg)
     Appointment_form = PatientAppointmentForm(request.POST or None, request.FILES or None, instance=Appointment)

     if Appointment_form.is_valid():
         Appointment_form.save()




def update_existing_appointment(data, request):
    try:
        appt = AppointmentRequest.objects.get(id=data.get("appointment_id"))
        appt = save_appointment(
            appt,
            appointment_number=appointment_number,
            status="Pending",
            fullname=full_name,
            email=email,
            mobile_number=mobile_number,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            worry_id=worry_instance,
            additional_msg=additional_msg,
            payment=payment,
            recommended_test=recommended_test,
            prescription=prescription,
            remark=remark,
            clinic=clinic,
            nerd=nerd,
            client_name=data.get("client_name"),
            request=request,
         )
        if not appt:
             return json_response("Service not offered by staff member.", status=400, success=False,
                                  error_code=ErrorCode.SERVICE_NOT_FOUND)
        appointments_json = convert_appointment_to_json(request, [appt])[0]
        return json_response(appt_updated_successfully, custom_data={'appt': appointments_json})
    except Appointment.DoesNotExist:
         return json_response("Appointment does not exist.", status=404, success=False,
                              error_code=ErrorCode.APPOINTMENT_NOT_FOUND)
    except Service.DoesNotExist:
         return json_response("Service does not exist.", status=404, success=False,
                              error_code=ErrorCode.SERVICE_NOT_FOUND)
    except Exception as e:
         return json_response(str(e.args[0]), status=400, success=False)



def send_sms(phone_number, message):
    try:
        username = 'Junction_Dental'
        api_key = 'your_api_key_here'  # Replace with environment variable
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS
        sms.send(message, [phone_number])
    except Exception as e:
        raise Exception(f"SMS sending failed: {str(e)}")

def appointment_success(request, appointment_number):
    appointment = get_object_or_404(AppointmentRequest, appointment_number=appointment_number)
    doctor_id = appointment.doctor_id
    page = Page.objects.all()
    email = appointment.email
    mobile_number = appointment.mobile_number
    appointment_details = AppointmentRequest.objects.filter(appointment_number=appointment_number)
    try:
        if User.objects.filter(email=email).exists() and User.objects.filter(mobile_number=mobile_number).exists():
            messages.success(request, f'Account exist on Membership Plan . Kindly Login to your Account of email  {email}')
            context = {'doctorview': doctor_id, 'appointment_details': appointment_details, 'page': page}
            return render(request, 'accounts/includes/appointment_success.html', context)
    except ValueError:
        messages.error(request, "Account not found")
        return redirect('register')  # Redirect back to the appointment page
    messages.error(request, f"An error occurred: {str(e)}")
    context = {'appointment': appointment}  # Add more context data as needed 
    return render(request, 'accounts/includes/appointment_success.html', context)






class AppointmentCancelView(View):
    def post(self, request, pk):
        appointment = get_object_or_404(
            Booking,
            pk=pk,
            patient=request.user,
            status__in=["pending", "confirmed"],
        )

        appointment.status = "cancelled"
        appointment.save()

        messages.success(request, "Appointment cancelled successfully")
        return redirect("patients:dashboard")


class AppointmentPrintView(DetailView):
    model = AppointmentRequest
    template_name = "appointment/appointment-print.html"
    context_object_name = "appointment"

    def get_queryset(self, **kwargs):
        return AppointmentRequest.objects.filter(appointment_number=self.kwargs["appointment_number"])

    def render_to_response(self, context):
        html_string = render_to_string(
            self.template_name, context, request=self.request
        )
        return HttpResponse(html_string)



class AppointmentDetailView(DetailView):
    model = Prescription
    template_name = "user_profile/includes/profile.html"
    context_object_name = "appointment"

    def get_queryset(self):
        return Booking.objects.select_related(
            "doctor", "doctor__profile", "patient", "patient__profile"
        ).filter(patient=self.request.user)

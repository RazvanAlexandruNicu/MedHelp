from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from users.models import extendedUser, User
from users.signals import create_appointment
from django.db.models import signals
from django.db.models.signals import post_save

from users.models import Appointment, Prescription
from .forms import UserRegisterForm, requestAppointmentForm, PrescriptionForm, DecideRequests, UserRegisterFormByAdmin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in! Your medic code {user.medic_code}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def add_member(request):
    if request.method == 'POST':
        form = UserRegisterFormByAdmin(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'The account for {username} has been created!')
            return redirect('blog-home')
    else:
        form = UserRegisterFormByAdmin()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    try:
        userr = extendedUser.objects.get(username=user.username)
    except extendedUser.DoesNotExist:
        userr = user
    if userr.username != "admin":
        medic = extendedUser.objects.get(medic_code=userr.medic_code, groups__name__in=['Medic'])
        return render(request, 'users/profile.html', {'user': userr, 'medic': medic})
    else:
        return render(request, 'users/profile.html', {'user': user})

@login_required
def add_prescription(request):
    user = request.user
    try:
        userr = extendedUser.objects.get(username=user.username)
    except extendedUser.DoesNotExist:
        userr = user

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            patient_name = form.cleaned_data['patient']
            x = patient_name.split(' ')
            patient = extendedUser.objects.get(username=x[0][1:-1])
            sub.user = patient
            sub.save()
            messages.success(request, 'Your prescription has been sent!')
            return redirect('blog-home')
    else:
        form = PrescriptionForm()

    patients = extendedUser.objects.filter(medic_code=userr.medic_code, groups__name__in=['Patient'])
    return render(request, 'users/addPrescription.html', {'user': userr, 'patients': patients, 'form': form})

@login_required
def send_request_appointment(request):
    if request.method == 'POST':
        form = requestAppointmentForm(request.POST)
        if form.is_valid():
            user = request.user
            try:
                userr = extendedUser.objects.get(username=user.username)
            except extendedUser.DoesNotExist:
                userr = user
            sub = form.save(commit=False)
            sub.user = userr
            sub.save()
            messages.success(request, 'Your appointment request has been sent!')
            return redirect('blog-home')
    else:
        form = requestAppointmentForm()
    return render(request, 'users/setAppointment.html', {'form': form})

@login_required
def view_requests(request):
    if request.method == 'POST':
        form = DecideRequests(request.POST)
        if form.is_valid():
            info = form.cleaned_data['info']
            #sub.save()
            responses = info.split(" ")

            for res in responses:
                pk, values = res.split("-")
                print(pk, values)
                o1, o2 = values.split(",")
                if o1 == "false" and o2 == 'true':
                    print(pk, "will be refused")
                    t = Appointment.objects.get(pk=pk)
                    t.pending = False
                    t.cancelled = True
                    post_save.disconnect(create_appointment, sender=Appointment)
                    t.save(update_fields=['pending', 'cancelled'])
                    post_save.connect(create_appointment, sender=Appointment)
                if o1 == "true" and o2 == 'false':
                    print(pk, "will be accepted")
                    t = Appointment.objects.get(pk=pk)
                    t.pending = False
                    t.cancelled = False
                    post_save.disconnect(create_appointment, sender=Appointment)
                    t.save(update_fields=['pending', 'cancelled'])
                    post_save.connect(create_appointment, sender=Appointment)

            messages.success(request, 'Your requests have successfully been resolved!')
            return redirect('blog-home')
    else:
        form = DecideRequests()
    user = request.user
    try:
        user = extendedUser.objects.get(username=user.username)
    except extendedUser.DoesNotExist:
        user = user

    patients = extendedUser.objects.filter(medic_code=user.medic_code, groups__name__in=['Patient'])
    all_requests = Appointment.objects.filter(pending=True)
    requests = []
    for req in all_requests:
        if req.user in patients:
            requests.append(req)

    return render(request, 'users/listRequests.html', {'form': form, 'user': user, 'requests': requests})

@login_required
def view_appointments(request):
    user = request.user
    try:
        userr = extendedUser.objects.get(username=user.username)
    except extendedUser.DoesNotExist:
        userr = user
    appointments = []
    if userr in extendedUser.objects.filter(groups__name__in=['Patient']):
        appointments = Appointment.objects.filter(user=user)
    if userr in extendedUser.objects.filter(groups__name__in=['Medic']):
        my_patients = extendedUser.objects.filter(medic_code=userr.medic_code, groups__name__in=['Patient'])
        for patient in my_patients:
            temp = Appointment.objects.filter(user=patient, pending=False, cancelled=False)
            if len(temp) > 0:
                for appointment in temp:
                    appointments.append(appointment)
    print(appointments)
    return render(request, 'users/listAppointments.html', {'appointments': appointments, 'user': user})

@login_required
def view_prescriptions(request):
    user = request.user
    prescriptions = []
    print(user.username)
    prescriptions = Prescription.objects.filter(user=user)
    return render(request, 'users/listPrescriptions.html', {'prescriptions': prescriptions, 'user': user})



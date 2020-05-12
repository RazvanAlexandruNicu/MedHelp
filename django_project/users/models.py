from django.db import models
from django.contrib.auth.models import User

class extendedUser(User):
    MEDIC = 'MD'
    PATIENT = 'PT'
    NONE = 'NN'
    CHOICES = [
       (NONE, 'Not Defined'),
       (MEDIC, 'Medic'),
       (PATIENT, 'Patient'),
    ]
    type = models.CharField(
       max_length=3,
       choices=CHOICES,
       default=NONE,
    )
    medic_code = models.CharField(max_length=20, default='')
    firstname = models.CharField(max_length=500, default='')
    lastname = models.CharField(max_length=500, default='')

class Profile(models.Model):
    user = models.OneToOneField(extendedUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Appointment(models.Model):
    pending = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=False)
    user = models.ForeignKey(extendedUser, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    description = models.CharField(max_length=500, default='')
    time = models.CharField(max_length=10, default='')

class Prescription(models.Model):
    description = models.CharField(max_length=500, default='')
    user = models.ForeignKey(extendedUser, on_delete=models.CASCADE, blank=True, null=True)
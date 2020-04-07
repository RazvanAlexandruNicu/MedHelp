from django.db import models
from django.contrib.auth.models import User

class extendedUser(User):
   # user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
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

class Profile(models.Model):
    user =  models.OneToOneField(extendedUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

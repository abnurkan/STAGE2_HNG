from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator, MinLengthValidator
import uuid
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,firstName, lastName,email,password=None,phone=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(firstName=firstName, lastName=lastName, email=email,phone=phone,password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, password):        
        return self.create_user(email, firstName, lastName, password)

class User(AbstractBaseUser):
    #userId = models.AutoField(primary_key=True)
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=30, validators=[MinLengthValidator(2)])
    lastName = models.CharField(max_length=30, validators=[MinLengthValidator(2)])
    email = models.EmailField(unique=True, validators=[EmailValidator()])      #must be unique
    password = models.CharField(max_length=15, validators=[MinLengthValidator(10)])
    phone = models.CharField(max_length=15, validators=[MinLengthValidator(10)])
    organisations = models.ManyToManyField('Organisation', related_name='users', blank=True)

    USERNAME_FIELD = 'email'  #Specifies that the email and password field should be used as the unique identifier for authentication.
    REQUIRED_FIELDS = ['firstName', 'lastName']

    objects = UserManager()

    def __str__(self):
        return self.email
# Define the Organisation Model

class Organisation(models.Model):
    orgId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

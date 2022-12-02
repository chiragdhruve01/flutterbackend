from django.db import models
from django.utils.translation import gettext_lazy  as _
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.timezone import get_default_timezone
import uuid

# Create your models here.
STATE = [
        ('AL','Alabama'),
        ('AK','Alaska'),
        ('AZ','Arizona'),
        ('AR','Arkansas'),
        ('CA','California'),
        ('CO','Colorado'),
        ('CT','Connecticut'),
        ('DE','Delware'),
        ('FL','Florida'),
        ('GA','Georgia'),
        ('HI','Hawaii'),
        ('ID','Idaho'),
        ('IL','Illinois'),
        ('IN','Indiana'),
        ('IA','Iowa'),
        ('KS','Kansas'),
        ('KY','Kentucky'),
        ('LA','Louisiana'),
        ('ME','Maine'),
        ('MD','Maryland'),
        ('MA','Massachusetts'),
        ('MI','Michigan'),
        ('MN','Minnesota'),
        ('MS','Mississippi'),
        ('MO','Missouri'),
        ('MT','Montana'),
        ('NE','Nebraska'),
        ('NV','Nevada'),
        ('NH','New Hampshire'),
        ('NJ','New Jersey'),
        ('NM','New Mexico'),
        ('NV','New York'),
        ('NC','North Carolina'),
        ('ND','North Dakota'),
        ('OH','Ohio'),
        ('OK','Oklahoma'),
        ('OR','Oregon'),
        ('PA','Pennsylvania'),
        ('RI','Rhode Island'),
        ('SC','South Carolina'),
        ('SD','South Dakota'),
        ('TN','Tennessee'),
        ('TX','Texas'),
        ('UT','Utah'),
        ('VT','Vermont'),
        ('VA','Virginia'),
        ('WA','Washington'),
        ('WV','West Virginia'),
        ('WI','Wisconsin'),
        ('WY','Wyoming'),
        ('AS','American Samoa'),
        ('DC','District of Columbia'),
        ('FM','Federated States of Micronesia'),
        ('GU','Guam'),
        ('MH','Marshall Islands'),
        ('MP','Northern Mariana Islands'),
        ('PW','Palau'),
        ('PR','Puerto Rico'),
        ('VI ','Virgin Islands'),
]

USER_TYPE = (
    ('superadmin','superadmin'),
    ('admin','admin'),
    ('user','user'),
)

class Country(models.Model):
    
    image = models.ImageField(upload_to='media/country',blank=True,null=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    place = models.CharField(max_length=50,blank=True,null=True)
    destination = models.CharField(max_length=50,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return str(self.place)


class State(models.Model):
    
    image = models.ImageField(upload_to='media/state',blank=True,null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, blank=True, null=True, related_name="country")
    name = models.CharField(max_length=50,blank=True,null=True)
    place = models.CharField(max_length=50,blank=True,null=True)
    destination = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.place)

class City(models.Model):
    
    image = models.ImageField(upload_to='media/city',blank=True,null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, blank=True, null=True, related_name="country1")
    state = models.ForeignKey('State', on_delete=models.SET_NULL, blank=True, null=True, related_name="state")
    name = models.CharField(max_length=50,blank=True,null=True)
    place = models.CharField(max_length=50,blank=True,null=True)
    destination = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.place)

class Area(models.Model):
    
    image = models.ImageField(upload_to='media/area',blank=True,null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, blank=True, null=True, related_name="country2")
    state = models.ForeignKey('State', on_delete=models.SET_NULL, blank=True, null=True, related_name="state1")
    city = models.ForeignKey('City', on_delete=models.SET_NULL, blank=True, null=True, related_name="city")
    name = models.CharField(max_length=50,blank=True,null=True)
    place = models.CharField(max_length=50,blank=True,null=True)
    destination = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.place)
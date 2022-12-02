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

class User(models.Model):
    
    image = models.ImageField(upload_to='media/users',blank=True,null=True)
    firstName = models.CharField(max_length=50,blank=True,null=True)
    middleName = models.CharField(max_length=50,blank=True,null=True) 
    lastName = models.CharField(max_length=50,blank=True,null=True) 
    contactPhone = models.CharField(max_length=15,blank=True,null=True)
    fax = models.CharField(max_length=15,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    companySite = models.CharField(max_length=50,blank=True,null=True)
    password = models.CharField(max_length=150,blank=True,null=True)

    language = models.CharField(max_length=50,blank=True,null=True)
    timeZone = models.CharField(max_length=50,blank=True,null=True)
    communication = models.CharField(max_length=50,blank=True,null=True)

    address1 = models.CharField(max_length=200,blank=True,null=True)
    address2 = models.CharField(max_length=200,blank=True,null=True)
    zipcode = models.IntegerField(blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(default="United States",max_length=50,blank=True,null=True)
    response = models.TextField(blank=True,null=True)
    county = models.CharField(max_length=150,blank=True,null=True)
    userType = models.CharField(max_length=150,choices=USER_TYPE,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    validityFrom = models.CharField(max_length=50,blank=True,null=True)
    validityTo = models.CharField(max_length=50,blank=True,null=True)
    is_active = models.BooleanField(default=False,blank=True,null=True)
    is_verified = models.BooleanField(default=False,blank=True,null=True)
    is_expire = models.BooleanField(default=False,blank=True,null=True)
    last_login = models.DateTimeField(verbose_name=_("last login"), auto_now=True)
    date_joined = models.DateTimeField(verbose_name=_("date joined"), auto_now_add=True)
    is_staff = models.BooleanField(default=False,blank=True,null=True)
    access_token = models.CharField(max_length=100, unique=True ,default=uuid.uuid4)
    device_info = models.CharField(max_length=250,blank=True,null=True)
    device_id = models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return str(self.id) + ' ' +str(self.firstName)

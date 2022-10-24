from django.db import models
from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.class AgentType(models.Model):

class AgentType(models.Model):
    slug = models.SlugField(max_length = 205,null =
     True,blank = True)
    type = models.CharField(max_length=200)
    type_image = models.ImageField(upload_to='type_images', null=True, blank=True)

    def __str__(self):
        return self.type

class Profile(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telephone_number = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='profile', null=True, blank=True)
    is_client = models.BooleanField(default=False)
    license = models.ImageField(upload_to='license', null=True, blank=True)
    is_agent = models.BooleanField(default=False)
    agent_type = models.ForeignKey(AgentType, on_delete=models.CASCADE, related_name='agents', null=True, blank=True)
    company = models.CharField(max_length=200,null=True,blank=True)
    company_description = models.TextField(null=True,blank=True)
    company_location = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,null = True,blank = True)
    region = models.CharField(max_length=200,null = True,blank = True)
    def __str__(self):
        return self.user.username

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=200,null = True,blank = True)
    date = models.DateTimeField(default=now)
    content = models.TextField(max_length = 250,null = True,blank = True)
    rating = models.DecimalField(max_digits = 2,decimal_places = 1,null = True,blank = True)
    def __str__(self):
        return self.name

class Order(models.Model):
    client_name = models.CharField(max_length=200)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date = models.DateTimeField(default=now)
    code = models.CharField(max_length=20, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    code_active = models.BooleanField(default=False)
    class Meta:
        ordering = ['date']
    def __str__(self):
        return self.client_name + ' working with ' + user.username + 'as an agent'


#   *** ACTIVATE VIRTUALENV BEFORE STARTING ***
#   REMEMBER TO KEEP NOTES IN PLAN IF REQUIRED
#   
#
#   ************ Homepage is basically done, maybe check responsiveness and add links on featured section once car pages done ************
#   ************ Change size and length of description field in Django admin ************
#
#   ************ Maybe start on the car details page, as showroom and index are basically finished - DO NOW**
#   ************ Links need to be added to the index page featured section cars after the car details page is finished


from django.db import models
from django.dispatch import receiver # for photo delete signal
from django.db.models.signals import pre_delete, pre_save # Used for receiving the pre_delete and pre_save signals
from uuid import uuid4 # Used to generate random bits
import os

# function used to change filename - used as callback for ImageField 
def rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return os.path.join('images/', filename)

# Create your models here.

class Make(models.Model):   # Model for car manufacturer
    manufacturer = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.manufacturer
    


class Model(models.Model):  # Model for car model
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name='model_name')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    

class Vehicle(models.Model):    # Model for specifications
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name='vehicles')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='vehicles')
    title = models.CharField(max_length=300)
    TRANS_CHOICES = (
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
        ('Semi-Automatic', 'Semi-Automatic')
    )
    transmission = models.CharField(max_length=300, choices=TRANS_CHOICES)
    mileage = models.PositiveIntegerField()
    engine = models.PositiveIntegerField(help_text="Please enter engine size as cc value - Example '1998' - Do not add cc at end of number.")
    FUEL_CHOICES = (
        ('BioFuel', 'BioFuel'),
        ('Hybrid-Petrol/Electric', 'Hybrid-Petrol/Electric'),
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Hybrid-Petrol/Electric Plug-in', 'Hybrid-Petrol/Electric Plug-in')
    )
    fuel_type = models.CharField(max_length=50, choices=FUEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    BODY_CHOICES = (
        ('Hatch', 'Hatchback'),
        ('Estate', 'Estate'),
        ('SUV', 'SUV'),
        ('Saloon', 'Saloon'),
        ('Coupe', 'Coupe'),
        ('Convert', 'Convertible'),
        ('MPV', 'MPV'),
        ('Pick', 'Pickup')
    )
    body_style = models.CharField(max_length=20, choices=BODY_CHOICES)
    colour = models.CharField(max_length=20) # add choice list in form
    doors = models.PositiveIntegerField() # add choice list in form
    seats = models.PositiveIntegerField() # add choice list in form
    insurance_group = models.PositiveIntegerField(help_text="Please enter insurance group in range of 1-50 - Enter numbers only.") # add choice list in form
    zero_sixty = models.DecimalField(max_digits=2, decimal_places=1, default=0, help_text="Enter numbers only - Example '4.6'")
    top_speed = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Enter number value only - Example '155'.") # add validation in form so only three digits can be entered
    desctiption = models.TextField()

    def __str__(self):
        return self.title
    


class Image(models.Model):  # Model used to store images
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to=rename)

    def __str__(self):
        return self.vehicle.title


@receiver(pre_delete, sender=Image) # Function used to delete image files after pre_delete signal received
def image_delete(sender, instance, **kwargs):
    instance.images.delete(False)


@receiver(pre_save, sender=Image)   # Function used to delete image files when pre_save signal received from Image model - Delete's image if new image different from old one
def delete_old_image_on_update(sender, instance, **kwargs):
    # if instance/row is being created, then do nothing
    if instance.id is None:
        pass

    # else if it is being modified
    else:
        current = instance
        previous = Image.objects.get(id=instance.id)

        # if previous image is not equal to the current image - delete previous
        if previous.images != current.images:
            previous.images.delete(False)
#   *** ACTIVATE VIRTUALENV BEFORE STARTING ***
#   REMEMBER TO KEEP NOTES IN PLAN IF REQUIRED
#   
#
#   ************ Homepage is basically done, maybe check responsiveness and add links on featured section once car pages done ************
#   ************ Change size and length of description field in Django admin ************
#
#   ************ Car page - ADD CAR DESCRIPTION DIV UNDER SPECS AND IMAGE DIV ON CAR PAGE **
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
    YEARS = (
        ("2021", "2021"),
        ("2020", "2020"), ("2019", "2019"), ("2018", "2018"), ("2017", "2017"), ("2016", "2016"), ("2015", "2015"), ("2014", "2014"), ("2013", "2013"), ("2012", "2012"), ("2011", "2011"),
        ("2010", "2010"), ("2009", "2009"), ("2008", "2008"), ("2007", "2007"), ("2006", "2006"), ("2005", "2005"), ("2004", "2004"), ("2003", "2003"), ("2002", "2002"), ("2001", "2001"),
        ("2000", "2000"), ("1999", "1999"), ("1998", "1998"), ("1997", "1997"), ("1996", "1996"), ("1995", "1995"), ("1994", "1994"), ("1993", "1993"), ("1992", "1992"), ("1991", "1991"),
        ("1990", "1990"), ("1989", "1989"), ("1988", "1988"), ("1987", "1987"), ("1986", "1986"), ("1985", "1985"), ("1984", "1984"), ("1983", "1983"), ("1982", "1982"), ("1981", "1981"),
        ("1980", "1980"), ("1979", "1979"), ("1978", "1978"), ("1977", "1977"), ("1976", "1976"), ("1975", "1975"), ("1974", "1974"), ("1973", "1973"), ("1972", "1972"), ("1971", "1971"),
        ("1970", "1970"), ("1969", "1969"), ("1968", "1968"), ("1967", "1967"), ("1966", "1966"), ("1965", "1965"), ("1964", "1964"), ("1963", "1963"), ("1962", "1962"), ("1961", "1961"),
        ("1960", "1960"), ("1959", "1959"), ("1958", "1958"), ("1957", "1957"), ("1956", "1956"), ("1955", "1955"), ("1954", "1954"), ("1953", "1953"), ("1952", "1952"), ("1951", "1951"),
        ("1950", "1950"), ("1949", "1949"), ("1948", "1948"), ("1947", "1947"), ("1946", "1946"), ("1945", "1945"), ("1944", "1944"), ("1943", "1943"), ("1942", "1942"), ("1941", "1941"),
        ("1940", "1940"), ("1939", "1939"), ("1938", "1938"), ("1937", "1937"), ("1936", "1936"), ("1935", "1935"), ("1934", "1934"), ("1933", "1933"), ("1932", "1932"), ("1931", "1931"),
        ("1930", "1930"), ("1929", "1929"), ("1928", "1928"), ("1927", "1927"), ("1926", "1926"), ("1925", "1925"), ("1924", "1924"), ("1923", "1923"), ("1922", "1922"), ("1921", "1921"),
        ("1920", "1920"), ("1919", "1919"), ("1918", "1918"), ("1917", "1917"), ("1916", "1916"), ("1915", "1915"), ("1914", "1914"), ("1913", "1913"), ("1912", "1912"), ("1911", "1911"),
        ("1910", "1910"), ("1909", "1909"), ("1908", "1908"), ("1907", "1907"), ("1906", "1906"), ("1905", "1905"), ("1904", "1904"), ("1903", "1903"), ("1902", "1902"), ("1901", "1901"),
        ("1900", "1900"), ("1899", "1899"), ("1898", "1898"), ("1897", "1897"), ("1896", "1896"), ("1895", "1895"), ("1894", "1894"), ("1893", "1893"), ("1892", "1892"), ("1891", "1891"),
        ("1890", "1890"),
    )
    year = models.CharField(max_length=6, choices=YEARS)
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
    top_speed = models.DecimalField(max_digits=5, decimal_places=1, default=0, help_text="Enter number value only - Example '155'.") # add validation in form so only three digits can be entered
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
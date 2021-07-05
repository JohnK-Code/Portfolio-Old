from django.contrib import admin
from .models import Vehicle, Make, Model, Image

# Register your models here.
#class VehicleInline(admin.TabularInline):
#    model = Vehicle
#
#class ImageAdmin(admin.ModelAdmin):
#    inlines = [
#        VehicleInline,
#    ]

#admin.site.register(Vehicle)
#admin.site.register(Make)
#admin.site.register(Model)
#admin.site.register(Image)




class ImageAdmin(admin.StackedInline): # create inline model - Image 
    model = Image

@admin.register(Vehicle) # add inline image model to vehicle - allows multiple images to be added to each vehicle at a time
class VehicleAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]


class ImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    ordering = ['manufacturer']

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    ordering = ['name']
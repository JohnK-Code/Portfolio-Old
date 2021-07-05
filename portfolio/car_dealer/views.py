from django.core.paginator import Paginator
from django.http import response
from django.shortcuts import render

from car_dealer.models import Make, Model, Vehicle

# Below list's of tuples are used to pass information to search forms - These are used as values for the select options in each search form
TRANS = [
    ('', 'Transmission'),
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
    ('Semi-Automatic', 'Semi-Automatic')
]

MIN = [
    ('', 'Min'),
    ('0', '£0'),
    ('1000', '£1000'),('2000', '£2000'),('3000', '£3000'),('4000', '£4000'),('5000', '£5000'),('10000', '£10000'),
    ('15000', '£15000'),('20000', '£20000'),('25000', '£25000'),('30000', '£30000'),('35000', '£35000'),('40000', '£40000'),
    ('45000', '£45000'),('50000', '£50000'),('55000', '£55000'),('60000', '£60000'),('65000', '£65000'),('70000', '£70000'),
    ('75000', '£75000'),('80000', '£80000'),('85000', '£85000'),('90000', '£90000'),('95000', '£95000'),
]

MAX = [
    ('', 'Max'),
    ('1000', '£1000'),('2000', '£2000'),('3000', '£3000'),('4000', '£4000'),('5000', '£5000'),('10000', '£10000'),
    ('15000', '£15000'),('20000', '£20000'),('25000', '£25000'),('30000', '£30000'),('35000', '£35000'),('40000', '£40000'),
    ('45000', '£45000'),('50000', '£50000'),('55000', '£55000'),('60000', '£60000'),('65000', '£65000'),('70000', '£70000'),
    ('75000', '£75000'),('80000', '£80000'),('85000', '£85000'),('90000', '£90000'),('95000', '£95000'),('100000', '£100000'),
]

MILEAGE = [
    ('', 'Mileage (MAX)'),
    ('10000', '10,000'),('20000', '20,000'),('30000', '30,000'),('40000', '40,000'),('50000', '50,000'),('60000', '60,000'),
    ('70000', '70,000'),('80000', '80,000'),('90000', '90,000'),('100000', '100,000'),('150000', '150,000'),
]

FUEL = [
    ('', 'Fuel'),
    ('BioFuel', 'BioFuel'),('Hybrid-Petrol/Electric', 'Hybrid-Petrol/Electric'),('Petrol', 'Petrol'),('Diesel', 'Diesel'),('Hybrid-Petrol/Electric Plug-in', 'Hybrid-Petrol/Electric Plug-in')
]

# Create your views here.


# view function used to pass data to index.html template
def index(request): 
    make = Make.objects.all().values_list('manufacturer', flat=True).order_by('manufacturer')

    return render(request, 'car_dealer/index.html', {
        "make_list": make,
        "trans_list": TRANS,
        "fuel_list": FUEL,
        "Mileage": MILEAGE,
        "MIN": MIN,
        "MAX": MAX,
        "cars": Vehicle.objects.all(),
    })


# Used to query database when car manufacturer selected in search form - ajax request - return data to search form model field.
def formMakeModel(request): 
    if request.is_ajax and request.method == "GET":  
        model = Model.objects.all().order_by('name')
        # get the car make from form via ajax request
        car_make = request.GET["car_make"]
        model = model.filter(make__manufacturer=car_make).values_list('name', flat=True)
        model = list(model) # queryset is changed to list
        return response.JsonResponse(model, safe=False)


# view function is used to get required data and pass it to the showroom.html template - used to render the page also
def showroom(request): 
    make = Make.objects.all().values_list('manufacturer', flat=True)
    query_list = Vehicle.objects.all().order_by('-id')

    count = query_list.count()

    paginator = Paginator(query_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'car_dealer/showroom.html', {
        "make_list": make,
        "trans_list": TRANS,
        "fuel_list": FUEL,
        "Mileage": MILEAGE,
        "MIN": MIN,
        "MAX": MAX,
        "count": count,
        'cars': page_obj
    })


# (GET form request) Used to handle the search form on the showroom page and show the results from the query carried out
def showroom_search(request): 
    make = Make.objects.all().values_list('manufacturer', flat=True)
    query_list = Vehicle.objects.all().order_by('-id')
    if 'search' in request.GET:
        if 'make' in request.GET:
            car_make = request.GET['make']
            if car_make:
                print("John " + car_make) #*******************
                query_list = query_list.filter(make__manufacturer=car_make)
        if 'model' in request.GET:
            car_model = request.GET['model']
            if car_model:
                print("John" + car_model) #*******************
                query_list = query_list.filter(model__name=car_model)
        if 'trans' in request.GET:
            car_trans = request.GET['trans']
            if car_trans:
                query_list = query_list.filter(transmission=car_trans)
        if 'fuel' in request.GET:
            car_fuel = request.GET['fuel']
            if car_fuel:
                query_list = query_list.filter(fuel_type=car_fuel)
        if 'mileage' in request.GET:
            car_mileage = request.GET['mileage']
            if car_mileage:
                query_list = query_list.filter(mileage__lte=car_mileage)
        if 'min' in request.GET:
            car_min = request.GET['min']
            if car_min:
                query_list = query_list.filter(price__gte=car_min)
        if 'max' in request.GET:
            car_max = request.GET['max']
            if car_max:
                query_list = query_list.filter(price__lte=car_max)
        
        
        count = query_list.count()

        paginator = Paginator(query_list, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = render(request, 'car_dealer/showroom.html', {
            "make_list": make,
            "trans_list": TRANS,
            "fuel_list": FUEL,
            "Mileage": MILEAGE,
            "MIN": MIN,
            "MAX": MAX,
            "count": count,
            'cars': page_obj
        })
        if 'make' in request.GET:
            response.set_cookie('make', car_make)
        if 'model' in request.GET:
            response.set_cookie('model', car_model)
        if 'trans' in request.GET:
            response.set_cookie('trans', car_trans)
        if 'fuel' in request.GET:
            response.set_cookie('fuel', car_fuel)
        if 'mileage' in request.GET:
            response.set_cookie('mileage', car_mileage)
        if 'min' in request.GET:
            response.set_cookie('min', car_min)
        if 'max' in request.GET:
            response.set_cookie('max', car_max)

        return response
    else:
        if 'make' in request.COOKIES:
            car_make = request.COOKIES['make']
            if car_make:
                query_list = query_list.filter(make__manufacturer=car_make)
        if 'model' in request.COOKIES:
            car_model = request.COOKIES['make']
            if car_model:
                query_list = query_list.filter(model__name=car_model)
        if 'trans' in request.COOKIES:
            car_trans = request.COOKIES['trans']
            if car_trans:
                query_list = query_list.filter(transmission=car_trans)
        if 'fuel' in request.COOKIES:
            car_fuel = request.COOKIES['fuel']
            if car_fuel:
                query_list = query_list.filter(fuel_type=car_fuel)
        if 'mileage' in request.COOKIES:
            car_mileage = request.COOKIES['mileage']
            if car_mileage:
                query_list = query_list.filter(mileage__lte=car_mileage)
        if 'min' in request.COOKIES:
            car_min = request.COOKIES['min']
            if car_min:
                query_list = query_list.filter(price__gte=car_min)
        if 'max' in request.COOKIES:
            car_max = request.COOKIES['max']
            if car_max:
                query_list = query_list.filter(price__lte=car_max)

        count = query_list.count()

        paginator = Paginator(query_list, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'car_dealer/showroom.html', {
            "make_list": make,
            "trans_list": TRANS,
            "fuel_list": FUEL,
            "Mileage": MILEAGE,
            "MIN": MIN,
            "MAX": MAX,
            "count": count,
            'cars': page_obj
        })




# view function is used to pass data to the car.html page and render it.
def car(request, id):   
    car = Vehicle.objects.get(id=id)
    return render(request, 'car_dealer/car.html', {
        'car': car
    })

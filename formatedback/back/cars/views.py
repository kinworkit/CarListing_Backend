from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Cars, VehicleModelYear, Complect
from .serializers import CarsSerializer, ComplectSerializer
from django.http import JsonResponse
from .car_data import PREDEFINED_KPP
from rest_framework import viewsets, generics


class CarsListView(generics.ListCreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer


class ComplectListView(generics.ListCreateAPIView):
    queryset = Complect.objects.all()
    serializer_class = ComplectSerializer


class ComplectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Complect.objects.all()
    serializer_class = ComplectSerializer

# Получение всех машин
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def car_list(request):
    if request.method == 'GET':
        marks = request.GET.getlist('marks[]')
        models = request.GET.getlist('models[]')
        years = request.GET.getlist('years[]')

        cars = Cars.objects.all()

        if marks:
            cars = cars.filter(vehicle_model_year__mark__in=marks)
        if models:
            cars = cars.filter(vehicle_model_year__model__in=models)
        if years:
            cars = cars.filter(vehicle_model_year__year__in=years)

        serializer = CarsSerializer(cars, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CarsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# круд для получения, обновления и удаления машин
@api_view(['GET', 'PUT', 'DELETE'])
def car_detail(request, pk):
    try:
        car = Cars.objects.get(pk=pk)
    except Cars.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = CarsSerializer(car)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CarsSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        car.delete()
        return Response(status=204)


# Search by parameters
@api_view(['GET'])
@permission_classes([AllowAny])
def car_search(request):
    if request.method == 'GET':
        transmission_type = request.GET.get('transmission_type')
        mark = request.GET.get('mark')
        model = request.GET.get('model')
        year = request.GET.get('year')
        city = request.GET.get('city')
        mileage_from = request.GET.get('mileage_from')
        mileage_to = request.GET.get('mileage_to')
        color = request.GET.get('color')
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')

        filter_params = Q()

        if transmission_type:
            filter_params &= Q(transmission_type=transmission_type)
        if mark:
            filter_params &= Q(mark__icontains=mark)
        if model:
            filter_params &= Q(model__icontains=model)
        if year:
            filter_params &= Q(year=year)
        if city:
            filter_params &= Q(city__icontains=city)
        if mileage_from:
            filter_params &= Q(mileage__gte=int(mileage_from))
        if mileage_to:
            filter_params &= Q(mileage__lte=int(mileage_to))
        if color:
            filter_params &= Q(color__icontains=color)
        if price_from:
            filter_params &= Q(price__gte=int(price_from))
        if price_to:
            filter_params &= Q(price__lte=int(price_to))

        cars = Cars.objects.filter(filter_params)

        response_data = [
            {
                'transmission_type': car.transmission_type,
                'mark': car.mark,
                'model': car.model,
                'year': car.year,
                'city': car.city,
                'price': car.formatted_price(),
                'mileage': car.formatted_mileage()
            }
            for car in cars
        ]

        return Response(response_data)


#up
def get_marks(request):
    marks = list(VehicleModelYear.objects.values_list('mark', flat=True).distinct())
    return JsonResponse(marks, safe=False)


def get_models(request):
    mark = request.GET.get('mark')
    models = list(VehicleModelYear.objects.filter(mark=mark).values_list('model', flat=True).distinct())
    return JsonResponse(models, safe=False)


def get_years(request):
    mark = request.GET.get('mark')
    model = request.GET.get('model')
    years = list(VehicleModelYear.objects.filter(mark=mark, model=model).values_list('year', flat=True).distinct())
    return JsonResponse(years, safe=False)


def get_kpp(request):
    kpps = [kpp[0] for kpp in PREDEFINED_KPP]
    return JsonResponse(kpps, safe=False)


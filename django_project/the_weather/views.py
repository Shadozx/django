from django.shortcuts import render, redirect
from .forms import CityForm
from . import models, forms
from django.contrib import messages
from .weather import get_weather


# вибір точної погоди
def choose(request):
    return render(request, 'choose.html')


# сторінка з відображення всіх доданих міст
def home_view(request):
    cities = models.City.objects.all()

    if request.method == "POST":

        form = forms.CityForm(request.POST)
        if form.is_valid():
            print("form is valid")
            form.save()

            # повідомлення про то що місто було успішно додане
            messages.success(request, "New city added")

            # перезавантажуємо поточнку сторінку
            return redirect('home_page')

    return render(request, 'home.html', context={'cities': cities})


# видалення міста
def delete_city(request, city_id):
    city = models.City.objects.get(pk=city_id)

    city.delete()

    # виведення повідомлення про то що місто було успішно видалене
    messages.success(request, "City deleted")

    # переходимо на домашню сторінку
    return redirect('home_page')


# фільтрація міст по вибраній погоді
def filter_cities(request):
    cities = models.City.objects.all()
    needed_weather = request.GET.get('field1')

    weather_data = []

    form = CityForm()

    for city in cities:
        # отримуємо потрібне місто
        city_weather = get_weather(str(city))

        keys = []

        for i in city_weather:
            for k in i:
                keys.append(k)

        sat = f'In {keys[0]} will be ' + city_weather[0][keys[0]]['temp']['maxtemp'] + '/' + \
              city_weather[0][keys[0]]['temp']['mintemp']
        sun = f'In {keys[1]} will be ' + ' ' + city_weather[1][keys[1]]['temp']['maxtemp'] + '/' + \
              city_weather[1][keys[1]]['temp']['mintemp']

        weather = {
            'city': city,
            'temperature': str(sat + ' and ' + sun),
            'description': {'sat': city_weather[0][keys[0]]['temp']['weather'],
                            'sun': city_weather[1][keys[1]]['temp']['weather']}
        }
        print(weather['description'])

        # додаємо інформацію про поточне місто до нашого списку
        weather_data.append(weather)

    # фільтруємо міста по вибраній погоді
    filtered_weather = []
    for weather in weather_data:
        if needed_weather == weather['description']['sat'] and needed_weather == weather['description']['sun']:
            filtered_weather.append(weather)

    print(filtered_weather)

    context = {'weather_data': filtered_weather, 'form': form}

    # виводимо відфільтровані міста
    return render(request, 'filtered.html', context)

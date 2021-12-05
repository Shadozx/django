import requests
from bs4 import BeautifulSoup

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


# отримання дані про погоду міста за допомогою парсинку сайта погоди
def get_weather(city):

    query = "weather.com " + city + " 10 days"
    url = ''

    for j in search(query, tld="co.in", num=2, stop=2, pause=1):
        if "https://weather.com/weather" in j:
            url = j

    # print(url)

    # отримуємо сторінку сайта
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    weather = soup.findAll('details', class_='Disclosure--themeList--25Q0H')
    new_weather = []
    for w in weather:
        new_weather.append(w.find('summary',
                                  class_='Disclosure--Summary--UuybP DaypartDetails--Summary--3IBUr Disclosure--hideBorderOnSummaryOpen--ZdSDc'))

    new_new_weather = []

    for w in new_weather:

        if w is not None:
            new_new_weather.append(
                w.find('div', class_='DetailsSummary--DetailsSummary--2HluQ DetailsSummary--fadeOnOpen--vFCc_'))

    final_weather = {}

    for data in new_new_weather:
        day = data.find('h2', class_="DetailsSummary--daypartName--2FBp2").text
        final_weather[day] = {}

        # сама погода
        weatherr = data.find('span', class_="DetailsSummary--extendedData--365A_").text
        w = data.find('div', class_="DetailsSummary--temperature--1Syw3")

        # максимальна температура
        tempHigh = w.find('span', class_="DetailsSummary--highTempValue--3Oteu").text

        # мінімальна температура
        tempLow = w.find('span', class_="DetailsSummary--lowTempValue--3H-7I").text
        hum = data.select_one("span[data-testid='PercentageValue']").text

        numberHigh = tempHigh.split('°')
        numberHigh = round((int(numberHigh[0]) - 32) / 1.8, 0)
        numberLow = tempLow.split('°')
        numberLow = round((int(numberLow[0]) - 32) / 1.8, 0)

        final_weather[day]['temp'] = {}
        final_weather[day]['temp']['maxtemp'] = str(numberHigh) + "°"
        final_weather[day]['temp']['mintemp'] = str(numberLow) + "°"
        final_weather[day]['temp']['weather'] = weatherr
        final_weather[day]['humudity'] = hum

    city_info = []
    amount = 0

    # фільтрація по вихідним дням
    for key in final_weather:
        if "Sat" in key:
            city_info.append({key: final_weather[key]})
            amount += 1
        elif "Sun" in key and amount == 1:
            city_info.append({key: final_weather[key]})
            break

    print(city_info)

    return city_info

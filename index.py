from tkinter import *
import requests #json files pip install requests
from datetime import datetime  
from datetime import timedelta 
from PIL import ImageTk,Image #images pip install pillow

root = Tk()
root.geometry("1050x700")
root.title("Super Pogoda")
root.iconbitmap("images/sun.ico")
#root.configure(bg="black")

smallFont = ("Verdana", 12)
bigFont = ("Verdana", 20, "bold")
veryBigFont = ("Verdana", 30, "bold")

cityInput = Entry(root, width=30, font = smallFont)
cityInput.grid(row=0, column=1, sticky="NW")

imgLabel = Label(root) 
imgLabel.grid(row=3, column=0)

def getCityIput():
    global city
    city = cityInput.get()
    getWeather(city)

def getWeather(city): #function to import data from api
    global imgLabel
    global img
    global icon_id

    api_key = "7b2dae7faa1f73d3bf36e806a21e20b2"
    units = "metric"
    lang = "pl"
    api ="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_key+"&units="+units+"&lang="+lang     #example: https://api.openweathermap.org/data/2.5/weather?q=london&appid=7b2dae7faa1f73d3bf36e806a21e20b2&units=metric&lang=pl
    json_data = requests.get(api).json()

    longitude = str(json_data['coord']['lon'])
    latitude = str(json_data['coord']['lat'])
    icon_id = json_data['weather'][0]['id']
    cityName = json_data['name'] +" "+ json_data['sys']["country"] + "\n" + str(datetime.date(datetime.now()))
    condition = json_data['weather'][0]['description']
    temperature = int(json_data['main']['temp'])
    min_temperature = int(json_data['main']['temp_min'])
    max_temperature = int(json_data['main']['temp_max'])
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']

    sunrise = datetime.fromtimestamp(int(json_data['sys']['sunrise'])).strftime("%H:%M:%S")
    sunset = datetime.fromtimestamp(int(json_data['sys']['sunset'])).strftime("%H:%M:%S")


    api2 = "http://api.openweathermap.org/data/2.5/air_pollution?lat="+latitude+"&lon="+longitude+"&appid="+api_key
    api3 = "http://api.openweathermap.org/data/2.5/forecast?q="+city+"&appid="+api_key+"&units="+units+"&lang="+lang 
    json_data_2 = requests.get(api2).json()
    json_data_3 = requests.get(api3).json()
    airPollution = json_data_2['list'][0]["main"]['aqi']
    airPollutionLabel1.config(text= "Jakość Powietrza: "), airPollutionLabel2.config(text = airPollutionIndex(airPollution)) 

    imgLabel.grid_forget()
    img = ImageTk.PhotoImage(Image.open("images/"+chooseImage(icon_id)+".png"))
    imgLabel = Label(root, image = img) 
    imgLabel.grid(row=2, column=0, columnspan=3)

    detailsWeather = "\n" + "Maksymalna temperatura: " + str(max_temperature) +"°C"+ "\n" + "Minimalna temperatura: " + str(min_temperature) +"°C"+ "\n" + "Ciśnienie: " + str(pressure) +"hPa"+ "\n" + "Wilgotność: " + str(humidity) +"%"+ "\n" + "Prędkość wiatru: " + str(wind) +"m/s"+ "\n" + "Wschód Słońca " + str(sunrise) + "\n" + "Zachód Słońca: " + str(sunset)

    cityNameLabel.config(text = cityName)
    mainWeatherLabel.config(text = condition)
    temperatureLabel.config(text = str(temperature) + "°C")
    detailsWeatherLabel.config(text = detailsWeather)
    
    weatherPrognosis=""

    for i in range(0, 33, 1):
        date_time_obj = datetime.strptime((json_data_3["list"][i]["dt_txt"]), '%Y-%m-%d %H:%M:%S')
        if(date_time_obj.hour == 15):
            temp = int(json_data_3["list"][i]["main"]["temp"])
            date_time_obj = date_time_obj.strftime("%Y-%m-%d") #%H:%M:%S
            weatherPrognosis += (str(date_time_obj)+ "   "  +str(round(temp))+"°C   "+ str(json_data_3["list"][i]["weather"][0]["description"])+ "\n")

    prognosisLabel.config(text = weatherPrognosis), prognosisTitleLabel.config(text = "Prognoza pogody 4 dniowa:" + "\n")

    cityInput.delete(0, 'end')

def airPollutionIndex(airPollution):
    match airPollution:
        case 1:
            airPollutionLabel2.config(fg="#156715")
            return "bardzo dobra"
        case 2:
            airPollutionLabel2.config(fg="#2CC327")
            return "dobra"
        case 3:
            airPollutionLabel2.config(fg="#F2F52A")
            return "poprawna"
        case 4:
            airPollutionLabel2.config(fg="#F5A82A")
            return "umiarkowana"
        case 4:
            airPollutionLabel2.config(fg="#B90000")
            return "zła"
        case 5:
            airPollutionLabel2.config(fg="#640000")
            return "bardzo zła"

def chooseImage(icon_id):
    if (int(icon_id)>=200 and int(icon_id)<300):
        return "Thunderstorm"
    elif (int(icon_id)>=300 and int(icon_id)<400):
        return "Drizzle"
    elif (int(icon_id)>=500 and int(icon_id)<600):
        return "Rain"
    elif (int(icon_id)>=600 and int(icon_id)<700):
        return "Snow"
    elif (int(icon_id)>=700 and int(icon_id)<800):
        return "Atmosphere"
    elif int(icon_id)==800:
        return "Clear"
    elif (int(icon_id)>=801 and int(icon_id)<900):
        return "Clouds"
    else:
        return "Default"

plsTypecity = Label(root, text="Podaj miasto:", font = smallFont)
cityNameLabel = Label(root, font = bigFont)
mainWeatherLabel = Label(root, font = bigFont)
temperatureLabel = Label(root, font = veryBigFont)
detailsWeatherLabel = Label(root, font = smallFont)
okButton = Button(root, text="ok", padx=5, pady=5, command=getCityIput)
airPollutionLabel1 = Label(root, font = smallFont)
airPollutionLabel2 = Label(root, font = smallFont)

prognosisTitleLabel = Label(root, font = bigFont)
prognosisLabel = Label(root, font = smallFont)

plsTypecity.grid(row=0, column=0, sticky="NW"), okButton.grid(row=0, column=2, sticky="NW") #0
cityNameLabel.grid(row=1, column=0, columnspan=3) #1
prognosisTitleLabel.grid(row=1, column=3) #2
mainWeatherLabel.grid(row=3, column=0, columnspan=3), prognosisLabel.grid(row=2, column=3, rowspan=2) #3
temperatureLabel.grid(row=4, column=0, columnspan=3)#4
detailsWeatherLabel.grid(row=5, column=0, columnspan=3)#5
airPollutionLabel1.grid(row=6, column=0, columnspan=3), airPollutionLabel2.grid(row=7, column=0, columnspan=3) #6,7

getWeather("Poznań")


root.mainloop()
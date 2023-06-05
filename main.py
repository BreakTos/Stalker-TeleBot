# You can Steal api keys sucker , IDC
from typing import Final
import wikipediaapi
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import requests
# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = '6288363813:AAG8Ic4vP4izH0_sR0prfrAWyJTQrEkuD5g'
BOT_USERNAME: Final = '@Stalk_Location_bot'


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! Let\'s start stalking')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s=update.message.text[6:]
    wiki=wikipediaapi.Wikipedia('en')
    page=wiki.page(s)
    if page.exists():
        page=(str)(page.summary)
        #page=page[0:300]
        page=page.split('\n')
        finalpage=page[0]
        #print(page[0])

        ans=""
        print(finalpage)
        if (finalpage[-1]==":"):
            await update.message.reply_text("Invalid Location")
            return
        if len(page[0])>300:
            finalpage=page[0][0:300]
            #print(finalpage)
            ch=page[0][300]
            x=300
            while(ch!='.' or (page[0][x+1].isdigit())):
                finalpage+=ch
                x+=1
                ch=page[0][x]
            else:
                finalpage+='.'
        ans+=finalpage+"\n";
    else:
        await update.message.reply_text("Invalid Location")
        return

    page=str(page)
    page=page.split()
    city_name=page[0]
    geolocator = Nominatim(user_agent="city_time_app")
    location = geolocator.geocode(city_name)


    if location:
        tf = TimezoneFinder()
        latitude, longitude = location.latitude, location.longitude
        timezone = pytz.timezone(tf.timezone_at(lng=longitude, lat=latitude))
        current_time = datetime.now(timezone)
        ans+="\nTime there is: "+current_time.strftime('%I:%M %p')+"\n"
        # api_key="40411b842e42a02d0908367c8b15e417"
        # url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
        # response = requests.get(url)
        # data = response.json()
        # print(data) #this is the open weather key which will be activated in few hours
        base_url = "http://api.weatherapi.com/v1"
        api_method = "/current.json"  # Replace with the desired API method
        api_key="1fbaa27387864c4fba7131924230306";
        url = f"{base_url}{api_method}?key={api_key}&q={latitude},{longitude}"
        response = requests.get(url)
        data = response.json()

        temperature_c = data['current']['temp_c']
        humidity = data['current']['humidity']
        wind_speed_kph = data['current']['wind_kph']
        condition = data['current']['condition']['text']
        print(temperature_c , humidity , wind_speed_kph , condition)
        ans+="Temperature: "+(str)(temperature_c)+" degree Celsius\n"
        ans+="Humidity: "+(str)(humidity)+"\n"
        ans+="Wind speed: "+(str)(wind_speed_kph)+" kms per hour\n"
        ans+="Sky: "+(str)(condition)+"\n"
    await update.message.reply_text(ans)
# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('stalk', custom_command))

    # Messages

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)

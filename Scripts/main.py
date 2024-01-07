import requests
from bs4 import BeautifulSoup
import os
import telebot
from env import os



bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['ingfo'])
def scrape(message):
    url = 'https://silat.fatisda.uns.ac.id/site/front'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the desired div element with class 'tab-pane' and id '2'
        div_element = soup.find('div', {'class': 'tab-pane', 'id': '2'})

        status = []
        ingfo = []
        if div_element:
            # Extract the data you need from the div element
            data = div_element.find('tbody').find_all('tr')
            for dt in data:
                status = dt['class']
                if(status[0]=='success'):
                    data_col_seq =dt.find_all('td', {'data-col-seq': ['1', '2', '5', '6', '7']})
                    res = [data.text.strip() for data in data_col_seq]
                    ingfo.append(res)
                else:
                    break

            if ingfo:
                for info in ingfo:
                    bot.reply_to(message, 
                    f"{'Tanggal:':<12} {info[0]}\n{'Mahasiswa:':<12} {info[1]}\n{'Jam:':<12} {info[2]} - {info[3]} \n{'Tempat:':<12} {info[4]}")
            else:
                bot.reply_to(message, "tidak ada semhas")
        else:
            bot.reply_to(message, "Div element with class 'tab-pane' and id '2' not found.")
    else:
        bot.reply_to(message, "Failed to retrieve the web page. Status code:", response.status_code)


bot.infinity_polling()


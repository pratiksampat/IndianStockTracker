import sys
import time
import telepot
from telepot.loop import MessageLoop

from datetime import datetime
from nsetools import Nse
nse = Nse()
stockList = {}
quantum = 5
initialTime = datetime.now()
myUsers = set([])
def handle(msg):
    currentTime = datetime.now()

    if currentTime.minute - initialTime.minute >= quantum and bool(stockList) and currentTime.hour > 9 and currentTime.hour < 16:
        initalTime = currentTime
        try :
            for keys in stockList[chat_id]:
                q = nse.get_quote(keys)
                if(stockList[chat_id][keys] < 0):    #i.e wait for the prices to go low
                    if int(q['lastPrice']) <= abs(stockList[keys]):
                        dispString = "Time to buy!!\n"+keys+" At price : "+stockList[chat_id][keys]
                        bot.sendMessage(chat_id, dispString)
                else :  #wait for prices to go up
                    if int(q['lastPrice']) >= abs(stockList[keys]):
                        dispString = "Time to Sell!!\n"+keys+" At price : "+stockList[chat_id][keys]
                        bot.sendMessage(chat_id, dispString)
        except :
            print("Nothing to do")


    content_type, chat_type, chat_id = telepot.glance(msg)
    myUsers.add(chat_id)
    print("Command : " + msg['text'], "Chat id : "  + str(chat_id), "\nTotal Users : " + str(len(myUsers)))

    if content_type == 'text':
        listParams = msg['text'].split()
        if listParams[0] in "/help":
            bot.sendMessage(chat_id,'''List of available commands.\n
1. /disp [NSECODE] 
        Displaying the current stock price.
        Eg : /disp ACC
2. /add [NSECODE] [% of gain/loss] [gain/loss (+/-)]
        Add a stock for tracking
        Eg : /add ACC 5 +
            Notify when the ACC stock goes 5 % or higher than it's current value
3. /list
        Shows the stocks currently being tracked with their latest values
4. /help
        Shows the list of available commands''')
        elif listParams[0] in "/disp":
            if len(listParams) == 2 and nse.is_valid_code(listParams[1]):
                q = nse.get_quote(listParams[1])
                
                price = "Current "+listParams[1]+" Price : " +str(q['lastPrice'])
                bot.sendMessage(chat_id, price)
            else:
                bot.sendMessage(chat_id, "Invalid Code")
        elif listParams[0] in "/add":
            if len(listParams) == 4 and nse.is_valid_code(listParams[1]):
                q = nse.get_quote(listParams[1])
                amt = (int(listParams[2])/100) * q['lastPrice']
                try:
                    if(listParams[3] == '-'):
                        stockList[chat_id][listParams[1]] = - (int(q['lastPrice']) - amt)
                    else:
                        stockList[chat_id][listParams[1]] = (int(q['lastPrice']) - amt)
                except:
                    stockList[chat_id] = {}
                    if(listParams[3] == '-'):
                        stockList[chat_id][listParams[1]] = - (int(q['lastPrice']) - amt)
                    else:
                        stockList[chat_id][listParams[1]] = (int(q['lastPrice']) - amt)
               
                dispString = "Added Stock : " + str(listParams[1]) + "\nTracking Price : "+ str(abs(stockList[chat_id][listParams[1]]))
                bot.sendMessage(chat_id,dispString)
            else :
                bot.sendMessage(chat_id, "Invalid Code")
        elif listParams[0] in "/list":
            try:
                for keys in stockList[chat_id]:
                    q = nse.get_quote(keys)
                    dispString = str(keys) +"\nCurrent Price : "+str(q['lastPrice'])+"\nDesired price : "+ str(abs(stockList[chat_id][keys]))
                    bot.sendMessage(chat_id,dispString) 
            except:
                bot.sendMessage(chat_id,"No stocks current being tracked.\nType /help to know how to add stocks for tracking")
        elif listParams[0] in "/start":
            bot.sendMessage(chat_id,"Welcome to the IndianStockBot Track your desired stocks for their prices and get notified when they cross your threshold!\nIf you are facing any difficulty type /help for help.")
        else :
            bot.sendMessage(chat_id,"Type /help for help")

bot = telepot.Bot('YOUR_BOT_KEY')
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)

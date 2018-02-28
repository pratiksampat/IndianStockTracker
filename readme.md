# NSE Indian Stock Tracker on Telegram

A telegram bot to track Indian NSE stocks and to notify teh user when the prices reaches the desired level to either buy or sell.

Hosted on Heroku using the telepot library and Nsetools API
> Telegram Username : @IndianStockBot

```haskell
Usage : List of available commands.

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
        Shows the list of available commands
```

TODO : 
1. Get the list of call NSE companies 
2. Stock Prediction Using ARIMA Models
3. Persistance in storage for all currently tracked stocks


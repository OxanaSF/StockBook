from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
import requests
import json
import os

def home(request):
    
    api_key = os.environ["KEY"]
    print(api_key)

    if request.method == 'POST':
        symbol = request.POST['symbol']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + symbol + "/quote?token="+ api_key)
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'symbol': "Enter a stock symbol"})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("The Stock Has Been Added!"))
            return redirect('add_stock')

    
    else:
        symbols = Stock.objects.all()
        print(symbols)
        output = []
        for symbol in symbols:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(symbol) + "/quote?token=pk_f70d962d090c45a1803dc7b0b7d4f8ac")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."


        return render(request, 'add_stock.html', {'symbols': symbols, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, (f"The { item } Stock Has Been Deleted!"))
    return redirect('add_stock')








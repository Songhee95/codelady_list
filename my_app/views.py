import requests
from bs4 import BeautifulSoup
# if user put space in the url,
# this quote_plus will fill the space with + in the url automatically
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

# Create your views here.

BASE_CRAIGSLIST_URL = "https://atlanta.craigslist.org/search/?query={}"


def home(request):
    return render(request, 'base.html')


def new_search(request):
    # request.POST returns dictionary
    search = request.POST.get('search')
    # all the searched text will be stored as an object in the search model
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # using requests library
    response = requests.get(final_url)
    data = response.text
    # Use BeautifulSoup to find value from html via className
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': "result-row"})
    post_title = post_listings[0].find(class_='result-title').text
    post_url = post_listings[0].find('a').get('href')
    post_price = post_listings[0].find(class_='result-price').text

    # store the data and send it to front-end

    print(post_title)
    print(post_url)
    print(post_price)

    # print(data)
    stuff_for_frontend = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

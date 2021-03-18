import requests
from bs4 import BeautifulSoup
# if user put space in the url,
# this quote_plus will fill the space with + in the url automatically
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

# Create your views here.

BASE_CRAIGSLIST_URL = "https://atlanta.craigslist.org/search/?query={}"
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


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

    # store the data and send it to front-end
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image = post.find(
                class_='result-image').get('data-ids').split(',')
            final_image = []
            for url in post_image:
                final_image.append((BASE_IMAGE_URL.format(url.split(':')[1])))
        else:
            final_image = ['https://craigslist.org/images/peace.jpg']

        final_postings.append((post_title, post_url, post_price, final_image))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

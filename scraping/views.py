from django.shortcuts import render, redirect
from .models import CategoryModel
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers import serialize

# For Scraping
import requests
import bs4


def home(request):
    if request.method == "POST":
        print("here")
        url = request.POST.get('url')

        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        features = []
        productName = soup.select('.B_NuCI')[0].getText()
        price = soup.select('._25b18c ._16Jk6d')[0].getText()
        if soup.select('._2o-xpa ._1mXcCf'):
            desc = soup.select('._2o-xpa ._1mXcCf')[0].getText()
        else:
            desc = ""

        if soup.select("._3kidJX img", src=True):
            image = soup.select("._3kidJX img", src=True)[0].attrs['src']
        else:
            image = soup.select("._312yBx img", src=True)[0].attrs['src']

        featuresList = soup.select("._2418kt li")

        if featuresList:
            for feature in featuresList:
                features.append(feature.getText())

        return JsonResponse({
            "productName": productName,
            "price": price,
            "desc": desc,
            "features": features,
            "image": image
        })

    context = {
        "categories": CategoryModel.objects.all()
    }
    return render(request, 'scraping/index.html', context=context)

def addCategory(request):
    res = requests.get('https://www.flipkart.com/')
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    categories = soup.select('._37M3Pb .xtXmba')
    try:
        for category in categories:
            CategoryModel.objects.create(
                category=category.getText()
            )
        messages.success(request, "Category scraped successfully!")
        return redirect('home')
    except:
        messages.error(request, "Error..Something went wrong")
        return redirect('home')

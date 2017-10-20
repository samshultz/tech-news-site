from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import NewsItem, Site


def news_list(request, site=None):
    news_items = NewsItem.objects.all().order_by("-date", "title")
    sites_list = Site.objects.all()


    if site:
        site = sites_list.filter(name=site)
        news_items = news_items.filter(site=site)

    paginator = Paginator(news_items, 30) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        news_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news_items = paginator.page(paginator.num_pages)
    context = {'news_items': news_items, "sites_list": sites_list}
    
    return render(request, 'updateinfo/index.html', context)

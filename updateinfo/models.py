from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        ordering = "name",

        
class NewsItem(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=300)
    site = models.ForeignKey(Site, related_name="news_item")
    date = models.DateField()


    def __str__(self):
        return self.title

    class Meta:
        ordering = "-date", "title"

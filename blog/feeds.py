from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    title = "Riitycoon Media Blog"
    link = "/blog/"
    description = "The latest posts from Riitycoon Media Blog."

    def items(self):
        return Post.objects.filter(status='published').order_by('-publish')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.publish.year, item.publish.month, item.publish.day, item.slug])

    def item_pubdate(self, item):
        return item.publish

from django.urls import path
from .feeds import LatestPostsFeed
from . import views
from .views import SearchResultsView
from .views import UpcomingEventsListView
from .views import (
    PostViewSet,
    CommentViewSet,
    PostCreateView,
    ReplyViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'replies', ReplyViewSet)

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('auth-api/', views.AuthenticationAPIView.as_view(), name='auth-api'),
    path('latest/feed/', LatestPostsFeed(), name='latest_posts_feed'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('admin/comment_list/', views.admin_comment_list, name='admin_comment_list'),
    path('react_to_reply/<int:reply_id>/<str:reaction>/', views.react_to_reply, name='react_to_reply'),
    path('politics/', views.category_post_list, {'category_name': 'politics'}, name='politics'),
    path('politics/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.category_post_detail, name='politics_detail'),
    path('entertainment/', views.category_post_list, {'category_name': 'entertainment'}, name='entertainment'),
    path('entertainment/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.category_post_detail, name='entertainment_detail'),
    path('business/', views.category_post_list, {'category_name': 'business'}, name='business'),
    path('business/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.category_post_detail, name='business_detail'),
    path('sports/', views.category_post_list, {'category_name': 'sports'}, name='sports'),
    path('sports/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.category_post_detail, name='sports_detail'),
    path('science_technology/', views.category_post_list, {'category_name': 'science_technology'}, name='science_technology'),
    path('science_technology/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.category_post_detail, name='science_technology_detail'),
    path('lifestyle/', views.category_post_list, {'category_name': 'lifestyle'}, name='lifestyle'),
    path('lifestyle/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.category_post_detail, name='lifestyle_detail'),
    path('education/', views.category_post_list, {'category_name': 'education'}, name='education'),
    path('education/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.category_post_detail, name='education_detail'),
    path('fashion/', views.category_post_list, {'category_name': 'fashion'}, name='fashion'),
    path('fashion/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.category_post_detail, name='fashion_detail'),
    path('media/compress/<int:media_id>/', views.compress_media, name='compress_media'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('search/', views.SearchFormView.as_view(), name='search'),
    path('recent/', views.recent_posts, name='recent_posts'),
    path('popular/', views.popular_posts, name='popular_posts'),
    path('archive/<int:year>/<int:month>/<int:day>/<category_name>/', views.archive, name='archive'),
    path('products/', views.featured_products, name='featured_products'),
    path('about/', views.about_us, name='about_us'),
    path('upcoming-events/', UpcomingEventsListView.as_view(), name='upcoming_events'),
    path('contact/', views.contact_us, name='contact_us'),
    path('advertisements/', views.advertisements, name='advertisements'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/like/', views.like_post, name='like_post'),
    path('blog/submit_comment/<int:post_id>/', views.submit_comment, name='submit_comment'),
    path('submit_reply/<str:comment_name>/', views.submit_reply, name='submit_reply'),
    path('blog/react/post/<int:post_id>/<str:reaction>/', views.react_to_post, name='react_to_post'),
    path('react/comment/<int:comment_id>/<str:reaction>/', views.react_to_comment, name='react_to_comment'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('<str:category_name>/', views.category_post_list, name='category_post_list'),
    path('submit_reply/<int:comment_id>/', views.submit_reply, name='submit_reply'),
    path('<str:category_name>/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.category_post_detail, name='category_post_detail'),
   
]

urlpatterns += router.urls

from rest_framework import generics, status
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.utils import timezone
from .forms import NewsletterSignupForm
from .forms import PostForm
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Category, Comment, Reply, Ad, Reaction
from .forms import CommentForm, ReplyForm
from .forms import ReactionForm
from .serializers import CategorySerializer, PostSerializer
from django.views.generic.edit import CreateView
from .forms import PostForm
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import CommentForm 
from rest_framework import viewsets
from urllib.parse import unquote
from rest_framework.permissions import IsAuthenticated 
from .serializers import ( 
PostSerializer,
CommentSerializer,
ProductSerializer,
EventSerializer,
MediaSerializer,
ReplySerializer,
)
from .models import ( Media,
Product,
Event,
Reaction,
Reply,
) 

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status='published')  # Filter only published posts
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]    


class PostCreateView(CreateView):
    template_name = 'create_post.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    permission_classes = [IsAuthenticated]

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
   
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    
class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
        
class UpcomingEventsListView(ListView):
    model = Event
    template_name = 'blog/sidebar/upcoming_events.html'
    context_object_name = 'upcoming_events'

    def get_queryset(self):
        return Event.objects.filter(date__gt=timezone.now()).order_by('date')[:5]

class SearchResultsView(ListView):
    template_name = 'blog/sidebar/search_results.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            post_results = Post.objects.filter(title__icontains=query)
            category_results = Category.objects.filter(name__icontains=query)
            post_results = [{'instance': post, 'type': 'Post'} for post in post_results]
            category_results = [{'instance': category, 'type': 'Category'} for category in category_results]
            results = post_results + category_results
        else:
            results = []
        
        return render(request, self.template_name, {'query': query, 'results': results})
    
class SearchFormView(View):
    template_name = 'blog/search_form.html'  # Your search form template

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        query = request.POST.get('q')
        results = Post.objects.filter(title__icontains=query)
        context = {'query': query, 'results': results}
        return render(request, self.template_name, context)


class AuthenticationAPIView(APIView):
    def delete(self, request, post_id):
        # Handle deleting a specific post
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        # Create a new post
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_id):
        # Update a specific post
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        # Delete a specific post
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def home(request):
    # Fetch only posts that are published and created in the past
    posts = Post.objects.filter(status='published')

    return render(request, 'blog/home.html', {'posts': posts})

def politics(request, year=None, month=None, day=None, slug=None):
    category_name = "Politics"

    if slug:
        return category_post_detail(request, category_name, year, month, day, slug)
    else:
        return category_post_list(request, category_name)
    
def entertainment(request, year=None, month=None, day=None, slug=None):
    category_name = "Entertainment"

    if slug:
        return category_post_detail(request, category_name, year, month, day, slug)
    else:
        return category_post_list(request, category_name)

def fashion(request, year=None, month=None, day=None, slug=None):
    category_name = "Fashion"

    if slug:
        return category_post_detail(request, category_name, year, month, day, slug)
    else:
        return category_post_list(request, category_name)


def sports(request, year=None, month=None, day=None, slug=None):
    category_name = "Sports"

    if slug:
        return category_post_detail(request, category_name, year, month, day, slug)
    else:
        return category_post_list(request, category_name)


def science_technology(request, year=None, month=None, day=None, slug=None):
    category_name = "Science_Technology"

    if slug:
        return category_post_detail(request, category_name, year, month, day, slug)
    else:
        return category_post_list(request, category_name)

def lifestyle(request, year=None, month=None, day=None, slug=None):
    category_name = "Lifestyle"

    if slug:
        return category_post_detail(request, category_name, year, month, day, slug)
    else:
        return category_post_list(request, category_name)


def education(request, year=None, month=None, day=None, slug=None):
    category_name = "Education"

    if slug:
        return category_post_detail(request, category_name, year, month, day, slug)
    else:
        return category_post_list(request, category_name)


def business(request, year=None, month=None, day=None, slug=None):
    category_name = "Business"

    if slug:
        return category_post_detail(request, category_name, year, month, day, slug)
    else:
        return category_post_list(request, category_name)


def get_category_name_from_post_slug(post_slug):
    # Logic to extract the category name from the post slug
    # For example, splitting the slug or any other method to extract the category name
    # This is just an example, you should adjust this based on how your slugs are structured
    parts = post_slug.split('-')  # Assuming your slug has hyphens separating different parts
    
    # Extract the category name from the slug (if it's in a specific position)
    category_name = parts[0]  # For example, if the category name is the first part of the slug
    
    return category_name

def like_post(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug
    )

    if request.method == 'POST':
        post.increase_likes()  # Increment the likes for the post
        post.save()  # Save the changes to the post

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def compress_media(request, media_id):
    media = Media.objects.get(pk=media_id)
    media.compress()  # Compress media based on its type

    # Redirect to the post detail page or any other page as needed
    return redirect('post_detail', pk=media.post.pk)  # Adjust 'post_detail' with your actual URL name

def submit_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Assign the comment to the post
            comment.save()

    # Get all approved comments for the post, including the newly added comment
    comments = post.comments.filter(active=True)
    
    # Add the post, comments, and comment form to the context
    context = {
        'post': post,
        'comments': comments,
        'comment_form': CommentForm(),  # Assuming you want to reset the form after submission
    }
    
    # Render the template with the updated context
    return render(request, 'blog/category_post_detail.html', context)

def submit_reply(request, comment_id):
    # Retrieve the parent comment
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            # Create a new reply object
            reply = form.save(commit=False)
            reply.comment = comment  # Associate the reply with the parent comment
            reply.save()
            return redirect('blog:category_post_detail', category_name=comment.post.category.name, year=comment.post.publish.year, month=comment.post.publish.month, day=comment.post.publish.day, slug=comment.post.slug)
    else:
        form = ReplyForm()
    
    return render(request, 'blog/submit_reply.html', {'form': form})

def get_category(request, category_name):
    print("Received category_name:", category_name)

    # Check for leading/trailing whitespaces
    print("Category name before retrieval:", category_name)

    try:
        # Attempt to retrieve the category
        category = get_object_or_404(Category, name__iexact=category_name)
    except Exception as e:
        print("Error:", e)
        category = None

    print("Retrieved category:", category)
    return category


def paginate_posts(request, posts):
    # Configure pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page = request.GET.get('page')

    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page.
        paginated_posts = paginator.page(paginator.num_pages)

    return paginated_posts

def get_post_detail_links(decoded_category_name, paginated_posts):
    post_detail_links = []
    for post in paginated_posts:
        post_detail_links.append({
            'title': post.title,
            'link': reverse('blog:category_post_detail', kwargs={
                'category_name': decoded_category_name,
                'year': post.publish.year,
                'month': post.publish.month,
                'day': post.publish.day,
                'slug': post.slug
            })
        })
    return post_detail_links



def category(request, category_name, year=None, month=None, day=None, slug=None):
    # Decoding category_name to handle special characters
    decoded_category_name = unquote(category_name)

    if slug:
        return category_post_detail(request, decoded_category_name, year, month, day, slug)
    else:
        return category_post_list(request, decoded_category_name)


def category_post_list(request, category_name):
    decoded_category_name = unquote(category_name)

    # Print statements for debugging
    print("Received category_name:", category_name)
    print("Decoded category_name:", decoded_category_name)

    category = get_category(request, decoded_category_name)

    # More print statements for debugging
    print("Retrieved category:", category)

    if category:
        # Retrieve posts for the category
        posts = Post.objects.filter(category=category, status='published')
        paginated_posts = paginate_posts(request, posts)

        categories = Category.objects.all()

        post_detail_links = get_post_detail_links(decoded_category_name, paginated_posts)

        return render(request, 'blog/category_post_list.html', {
            'posts': paginated_posts,
            'category': category,
            'categories': categories,
            'post_detail_links': post_detail_links
        })
    else:
        # Handle the case where the category is not found
        print("Category not found in the database.")
        return render(request, 'blog/category_not_found.html')


def category_post_detail(request, category_name, year, month, day, slug):
    category = get_category(request, category_name)

    if category:
        post = get_object_or_404(Post, slug=slug, publish__year=year, publish__month=month, publish__day=day, category=category)

        # Fetch other posts from the same category
        other_posts = Post.objects.filter(category=category, status='published').exclude(slug=post.slug).order_by('-publish')[:3]

        # Fetch comments for the post
        comments = post.comments.filter(active=True)

        # Handle comment submission
        if request.method == 'POST' and 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()

                # Redirect to the same post detail page after adding a comment
                return HttpResponseRedirect(reverse('blog:category_post_detail', kwargs={
                    'category_name': category.name,
                    'year': post.publish.year,
                    'month': post.publish.month,
                    'day': post.publish.day,
                    'slug': post.slug,
                }))

        # Handle reply submission
        elif request.method == 'POST' and 'reply' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                parent_comment_name = request.POST.get('parent_comment_name')
                parent_comment = get_object_or_404(Comment, name=parent_comment_name)
                new_reply = reply_form.save(commit=False)
                new_reply.comment = parent_comment
                new_reply.save()

                # Redirect to the same post detail page after adding a reply
                return HttpResponseRedirect(reverse('blog:category_post_detail', kwargs={
                    'category_name': category.name,
                    'year': post.publish.year,
                    'month': post.publish.month,
                    'day': post.publish.day,
                    'slug': post.slug,
                }))

        # Handle reactions
        elif request.method == 'POST' and 'reaction' in request.POST:
            reaction_type = request.POST.get('reaction')
            post.handle_reaction(reaction_type)

            # Redirect to the same post detail page after reacting
            return HttpResponseRedirect(reverse('blog:category_post_detail', kwargs={
                'category_name': category.name,
                'year': post.publish.year,
                'month': post.publish.month,
                'day': post.publish.day,
                'slug': post.slug,
            }))

        else:
            comment_form = CommentForm()
            reply_form = ReplyForm()

        # Calculate total reactions count
        total_reactions = post.likes + post.loves + post.wows + post.sads + post.angrys + post.cares

        context = {
            'post': post,
            'comments': comments,
            'category': category,
            'other_posts': other_posts,
            'comment_form': comment_form,
            'reply_form': reply_form,
            'total_reactions': total_reactions,
        }

        return render(request, 'blog/category_post_detail.html', context)

    else:
        # Handle the case where the category is not found
        # You may render an error page or redirect to another view
        return render(request, 'blog/category_not_found.html')



def react_to_post(request, post_id, reaction):
    # Retrieve the post object
    post = get_object_or_404(Post, pk=post_id)

    # Perform the reaction logic based on the 'reaction' parameter
    if reaction == 'like':
        post.likes += 1
    elif reaction == 'love':
        post.loves += 1
    elif reaction == 'care':
        post.cares += 1
    elif reaction == 'angry':
        post.angrys += 1
    elif reaction == 'wow':
        post.wows += 1
    elif reaction == 'sad':
        post.sads += 1
    elif reaction == 'laugh':
        post.laughs += 1
    # Add more conditions for other reactions if needed

    # Save the updated post object
    post.save()

    # Redirect to the category post detail page
    return redirect('blog:category_post_detail', category_name=post.category.name, year=post.publish.year, month=post.publish.month, day=post.publish.day, slug=post.slug)

def react_to_comment(request, comment_id, reaction):
    # Retrieve the comment object
    comment = get_object_or_404(Comment, pk=comment_id)

    # Perform the reaction logic based on the 'reaction' parameter
    if reaction == 'like':
        comment.likes += 1
    elif reaction == 'love':
        comment.loves += 1
    elif reaction == 'care':
        comment.cares += 1
    elif reaction == 'angry':
        comment.angrys += 1
    elif reaction == 'wow':
        comment.wows += 1
    elif reaction == 'sad':
        comment.sads += 1
    elif reaction == 'laugh':
        comment.laughs += 1
    # Add more conditions for other reactions if needed

    # Save the updated comment object
    comment.save()

    # Redirect to the category post detail page
    return redirect('blog:category_post_detail', category_name=comment.post.category.name, year=comment.post.publish.year, month=comment.post.publish.month, day=comment.post.publish.day, slug=comment.post.slug)

def react_to_reply(request, reply_id, reaction):
    # Retrieve the reply object
    reply = get_object_or_404(Reply, pk=reply_id)

    # Perform the reaction logic based on the 'reaction' parameter
    if reaction == 'like':
        reply.likes += 1
    elif reaction == 'love':
        reply.loves += 1
    elif reaction == 'care':
        reply.cares += 1
    elif reaction == 'angry':
        reply.angrys += 1
    elif reaction == 'wow':
        reply.wows += 1
    elif reaction == 'sad':
        reply.sads += 1
    elif reaction == 'laugh':
        reply.laughs += 1
    # Add more conditions for other reactions if needed

    # Save the updated reply object
    reply.save()

    # Redirect to the category post detail page (or wherever you want)
    return redirect('blog:category_post_detail', 
                    category_name=reply.comment.post.category.name, 
                    year=reply.comment.post.publish.year, 
                    month=reply.comment.post.publish.month, 
                    day=reply.comment.post.publish.day, 
                    slug=reply.comment.post.slug)

def admin_comment_list(request):
    comments = Comment.objects.filter(approved=False)
    return render(request, 'admin/comment_list.html', {'comments': comments})
    
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', year=post.publish.year, month=post.publish.month, day=post.publish.day, slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

def sidebar(request):
       
    return render(request, 'blog/sidebar/sidebar.html')

def archive(request, year=None, month=None, day=None, category_name=None):
    if category_name == 'all':
        # Retrieve all posts without filtering by category
        posts = Post.objects.filter(status='published')
    else:
        # Add logic here to filter posts by the specified category
        posts = Post.objects.filter(category__name__iexact=category_name, status='published')

    paginated_posts = paginate_posts(request, posts)
    categories = Category.objects.all()
    post_detail_links = get_post_detail_links(None, paginated_posts)

    return render(request, 'blog/category_post_list.html', {
        'posts': paginated_posts,
        'categories': categories,
        'post_detail_links': post_detail_links,
        'category_name': category_name,
    })

def popular_posts(request):
    popular_posts = Post.objects.filter(views_count__gte=100)  # Get posts with views greater than or equal to 100

    # Add category information to each popular post
    for post in popular_posts:
        post.category_name = post.category.name.lower()

    return render(request, 'blog/sidebar/popular_posts.html', {'popular_posts': popular_posts})


def recent_posts(request):
    recent_posts = Post.objects.order_by('-publish')[:5]  # Get the 5 most recent posts
    print(recent_posts)  # Add this line for debugging
    return render(request, 'blog/sidebar/recent_posts.html', {'recent_posts': recent_posts})



def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Process the form data (e.g., save to the database, send confirmation email)
            # Example: NewsletterSubscription.objects.create(email=email)

            # Render a success message or redirect the user to a thank you page
            return render(request, 'blog/sidebar/newsletter_success.html')
    else:
        form = NewsletterSignupForm()

    return render(request, 'blog/sidebar/newsletter_signup.html', {'form': form})


def featured_products(request):
    featured_products = Product.objects.filter(is_featured=True)[:5]
    return render(request, 'blog/sidebar/featured_products.html', {'featured_products': featured_products})

def about_us(request):
    about_content = {
        'title': 'About Riitycoon',
        'description': ("At Riitycoon, we are more than just a news service provider. "
                        "We are a dynamic team passionate about delivering the latest and "
                        "most reliable news updates to our audience. Our commitment extends "
                        "beyond news reporting; we pride ourselves on offering comprehensive "
                        "insights, analysis, and engaging content that keeps our readers informed "
                        "and empowered."),
        'services': {
            'news_services': ("Our core competency lies in delivering high-quality, unbiased news "
                              "across diverse domains. From global events to local stories, we strive "
                              "to bring factual, comprehensive, and up-to-date information to our readers."),
            'web_dev_and_prog': ("Beyond news reporting, our expertise branches into technology. Our dedicated "
                                 "development team excels in crafting innovative solutions for web development "
                                 "and programming services. Whether it's building dynamic websites, creating custom "
                                 "applications, or providing expert programming solutions, our team is equipped "
                                 "with the skills and knowledge to meet your technological needs."),
        },
        'mission': ("At Riitycoon, we endeavor to set new standards in journalism and technology. "
                    "Our mission is to combine the power of credible reporting with cutting-edge technology "
                    "to create a seamless experience for our audience. We aim to bridge the gap between "
                    "information and innovation, empowering our readers and clients through insightful content "
                    "and robust technological solutions."),
        'reasons_to_choose': {
            'reliable_reporting': ("Reliable Reporting: We uphold the highest standards of journalism, ensuring "
                                   "that our news content is accurate, trustworthy, and impartial."),
            'innovation_expertise': ("Innovation and Expertise: Our development team brings innovation and expertise "
                                     "to the table, delivering custom web development and programming services tailored "
                                     "to your needs."),
            'dedication_to_excellence': ("Dedication to Excellence: We are committed to excellence in all that we do, "
                                          "striving to exceed expectations and deliver unparalleled value to our audience "
                                          "and clients."),
        },
    }
    
    return render(request, 'blog/sidebar/about.html', {'about_content': about_content})

def contact_us(request):
    contact_info = {
        'email': 'info@riitycoon.media',
        'whatsapp': '+2348169814048',
        'location': 'Nigeria'
    }
    return render(request, 'blog/sidebar/contact.html', {'contact_info': contact_info})

def advertisements(request):
    # Implement your advertisements logic if needed
    return render(request, 'blog/sidebar/advertisements.html', {})


def submit_reply(request, comment_name):
    # Retrieve the comment based on the comment_name
    comment = get_object_or_404(Comment, name=comment_name)

    if request.method == 'POST':
        # Create an instance of your ReplyForm with the form data
        form = ReplyForm(request.POST)
        if form.is_valid():
            # Create a new reply instance but don't save it yet
            new_reply = form.save(commit=False)
            
            # Assign the comment to the reply
            new_reply.comment = comment
            
            # Save the reply
            new_reply.save()

            messages.success(request, 'Reply submitted successfully.')
            # Redirect to the appropriate page after submitting the reply
            return redirect(comment.get_absolute_url())
        else:
            messages.error(request, 'Error submitting the reply. Please check the form.')
    else:
        # If the request is not POST, create a new instance of your ReplyForm
        form = ReplyForm()

    return render(request, 'blog/submit_reply.html', {'form': form})


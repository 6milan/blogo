from django import forms
from .models import Comment, Post, Product, Event, Reply, Reaction

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'content', 'slug', 'image', 'media', 'category', 'status')  # Include 'category' and 'status' fields

        widgets = {
            'media': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # You can add additional widgets or modify existing ones for other fields here
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('name', 'email', 'body')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'is_featured')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date', 'location')

class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)

class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['reaction_type', 'post', 'comment']
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['name', 'email', 'body']
        labels = {
            'name': 'Your name',
            'email': 'Your email',
            'body': 'Your reply',
        }
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
            'body': forms.Textarea(attrs={'autocomplete': 'comment'}),
        }


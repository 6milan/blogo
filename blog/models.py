from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']  # You can change this to other fields if needed

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_post_list', args=[self.name.lower()])
    
class Media(models.Model):
    media_type = models.CharField(max_length=20)
    file = models.FileField(upload_to='media/')

    @property
    def url(self):
        return self.file.url

    def __str__(self):
        return f"{self.media_type}"

    def save(self, *args, **kwargs):
        if isinstance(self.file, memoryview):
            self.file = ContentFile(self.file.tobytes())

        super().save(*args, **kwargs)


    def compress(self):
        if 'video' in self.media_type:
            input_video_path = self.file.path
            output_video_path = os.path.join(settings.MEDIA_ROOT, 'compressed_videos', self.file.name)

            input_video = VideoFileClip(input_video_path)
            output_video = input_video.resize(width=640, height=480)
            output_video.write_videofile(output_video_path)

            # Update the file field with the compressed video
            self.file = 'compressed_videos/' + self.file.name
            self.save()

        elif 'audio' in self.media_type:
            input_audio_path = self.file.path
            output_audio_path = os.path.join(settings.MEDIA_ROOT, 'compressed_audios', self.file.name)

            audio = AudioSegment.from_file(input_audio_path, format=self.media_type)
            audio.export(output_audio_path, format="mp3", bitrate="64k")

            # Update the file field with the compressed audio
            self.file = 'compressed_audios/' + self.file.name
            self.save()

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='posts/images/')
    video_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)
    
    @staticmethod
    def get_category_choices():
        dynamic_categories = Category.objects.values_list('name', 'name')
        predefined_categories = [
            ('1', 'Politics'),
            ('2', 'Sports'),
            ('3', 'Entertainment'),
            ('4', 'Fashion'),
            ('5', 'Science_Technology'),
            ('6', 'Lifestyle'),
            ('7', 'Education'),
            ('8', 'Business'),
        ]
        return list(dynamic_categories) + predefined_categories

    CATEGORY_CHOICES = get_category_choices()
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    media = models.ManyToManyField(Media, related_name='posts')
    
    def get_media_urls(self):
        return [media.url for media in self.media.all()]

    def get_embedded_media(self):
        embedded_media = ""
        for media in self.media.all():
            if media.media_type == 'video':
                embedded_media += f'<video controls><source src="{media.url}" type="video/mp4"></video>'
            elif media.media_type == 'audio':
                embedded_media += f'<audio controls><source src="{media.url}" type="audio/mp3"></audio>'
        return embedded_media

    class Meta:
        verbose_name_plural = "Post"

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    likes = models.PositiveIntegerField(default=0)
    loves = models.PositiveIntegerField(default=0)
    cares = models.PositiveIntegerField(default=0)
    angrys = models.PositiveIntegerField(default=0)
    wows = models.PositiveIntegerField(default=0)
    sads = models.PositiveIntegerField(default=0)
    laughs = models.PositiveIntegerField(default=0)
    
    def increase_likes(self):
        self.likes += 1
        self.save()

    def increase_loves(self):
        self.loves += 1
        self.save()

    def increase_cares(self):
        self.cares += 1
        self.save()

    def increase_angrys(self):
        self.angrys += 1
        self.save()

    def increase_wows(self):
        self.wows += 1
        self.save()

    def increase_sads(self):
        self.sads += 1
        self.save()

    def increase_laughs(self):
        self.laughs += 1
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:category_post_detail', kwargs={
            'category_name': self.category.name.lower(),
            'year': self.publish.year,
            'month': self.publish.month,
            'day': self.publish.day,
            'slug': self.slug,
        })

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            max_size = (300, 300)
            img = Image.open(self.image)

            if img.height > max_size[0] or img.width > max_size[1]:
                img = img.resize(max_size, Image.BICUBIC)

                image_io = BytesIO()
                img.save(image_io, format='JPEG', quality=70)
                image_content = File(image_io, name=f'{self.slug}.jpg')

                self.image.save(f'{self.slug}.jpg', image_content, save=False)

        
        if self.media.exists():
            for media_file in self.media.all():
                if 'video' in media_file.media_type:
                    input_video_path = os.path.join(settings.MEDIA_ROOT, str(media_file.file))
                    output_video_path = os.path.join(settings.MEDIA_ROOT, 'compressed_videos', str(media_file.file))

                    input_video = VideoFileClip(input_video_path)
                    output_video = input_video.resize(width=640, height=480)
                    output_video.write_videofile(output_video_path)

                    media_file.file = 'compressed_videos/' + str(media_file.file)
                    media_file.save()

                elif 'audio' in media_file.media_type:
                    input_audio_path = os.path.join(settings.MEDIA_ROOT, str(media_file.file))
                    output_audio_path = os.path.join(settings.MEDIA_ROOT, 'compressed_audios', str(media_file.file))

                    audio = AudioSegment.from_file(input_audio_path, format=media_file.media_type)
                    audio.export(output_audio_path, format="mp3", bitrate="64k")

                    media_file.file = 'compressed_audios/' + str(media_file.file)
                    media_file.save()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))  # Add unique constraint
    email = models.EmailField(verbose_name=_('Email'))
    body = models.TextField(max_length=400, verbose_name=_('Body'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))
    active = models.BooleanField(default=False, verbose_name=_('Active'))
    likes = models.PositiveIntegerField(default=0, verbose_name=_('Likes'))
    loves = models.PositiveIntegerField(default=0, verbose_name=_('Loves'))
    cares = models.PositiveIntegerField(default=0, verbose_name=_('Cares'))
    angrys = models.PositiveIntegerField(default=0, verbose_name=_('Angrys'))
    wows = models.PositiveIntegerField(default=0, verbose_name=_('Wows'))
    sads = models.PositiveIntegerField(default=0, verbose_name=_('Sads'))
    laughs = models.PositiveIntegerField(default=0, verbose_name=_('Laughs'))
    
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies_to')

    class Meta:
        ordering = ['created_on']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'Comment {self.name} on {self.post}'

    def increase_likes(self):
        self.likes += 1
        self.save()

    def increase_loves(self):
        self.loves += 1
        self.save()

    def increase_cares(self):
        self.cares += 1
        self.save()

    def increase_angrys(self):
        self.angrys += 1
        self.save()

    def increase_wows(self):
        self.wows += 1
        self.save()

    def increase_sads(self):
        self.sads += 1
        self.save()

    def increase_laughs(self):
        self.laughs += 1
        self.save()

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    name = models.CharField(max_length=80, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    active = models.BooleanField(default=True, verbose_name=_('Active'))
    body = models.TextField(verbose_name=_('Body'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))
    likes = models.PositiveIntegerField(default=0, verbose_name=_('Likes'))
    loves = models.PositiveIntegerField(default=0, verbose_name=_('Loves'))
    cares = models.PositiveIntegerField(default=0, verbose_name=_('Cares'))
    angrys = models.PositiveIntegerField(default=0, verbose_name=_('Angrys'))
    wows = models.PositiveIntegerField(default=0, verbose_name=_('Wows'))
    sads = models.PositiveIntegerField(default=0, verbose_name=_('Sads'))
    laughs = models.PositiveIntegerField(default=0, verbose_name=_('Laughs'))
    
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies_to')

    class Meta:
        ordering = ['created_on']
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')

    def __str__(self):
        return f'Reply by {self.name} on {self.comment}'

    def increase_likes(self):
        self.likes += 1
        self.save()

    def increase_loves(self):
        self.loves += 1
        self.save()

    def increase_cares(self):
        self.cares += 1
        self.save()

    def increase_angrys(self):
        self.angrys += 1
        self.save()

    def increase_wows(self):
        self.wows += 1
        self.save()

    def increase_sads(self):
        self.sads += 1
        self.save()

    def increase_laughs(self):
        self.laughs += 1
        self.save()

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    purchase_link = models.URLField(blank=True)  # New field for the purchase link
    is_downloadable = models.BooleanField(default=False, verbose_name='Is Downloadable?')
    # Add a field for delivery type
    DELIVERY_CHOICES = [
        ('downloadable', 'Downloadable'),
        ('physical', 'Physical Delivery via Mail'),
        # Add more options if needed
    ]
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    views_count = views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Ad(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', _('Like')),
        ('love', _('Love')),
        ('care', _('Care')),
        ('angry', _('Angry')),
        ('wow', _('Wow')),
        ('sad', _('Sad')),
        ('laugh', _('Laugh')),
    ]
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.post:
            return f'{self.get_reaction_type_display()} on Post "{self.post.title}"'
        elif self.comment:
            return f'{self.get_reaction_type_display()} on Comment "{self.comment.body}"'
        else:
            return 'Invalid Reaction'

    class Meta:
        unique_together = ['post', 'comment']
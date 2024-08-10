from django.db import models
from .constants import BOOK_RATING
from .constants import BOOK_CATEGORY
from django.utils.text import slugify

# Create your models here.
class BookCategoryModel(models.Model):
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=False, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category}"
    

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(default="")
    price = models.IntegerField(default=0)
    ratings = models.IntegerField(choices=BOOK_RATING)
    book_category = models.ForeignKey(to=BookCategoryModel, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="media/", blank=True, null=True)
    isborrow = models.BooleanField(default=False)
    isreturned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"Comment is Done By {self.name}"

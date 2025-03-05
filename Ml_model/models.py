from django.db import models
from admin_app.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=255, db_column='Book-Title',null=True, blank=True)
    author = models.CharField(max_length=255, db_column='Book-Author',null=True, blank=True)
    year_of_publication = models.IntegerField(db_column='Year-Of-Publication',null=True, blank=True)
    publisher = models.CharField(max_length=255,null=True, blank=True)
    image_url_s = models.URLField(max_length=255, db_column='Image-URL-S', null=True, blank=True)
    image_url_m = models.URLField(max_length=255, db_column='Image-URL-M', null=True, blank=True)
    image_url_l = models.URLField(max_length=255, db_column='Image-URL-L', null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        db_table = 'books'

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'ratings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name = 'ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.user_id} rated {self.book_isbn} {self.rating} stars"

    class Meta:
        db_table = 'Rating'
        unique_together = ('user', 'book')
        

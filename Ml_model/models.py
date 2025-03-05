from django.db import models

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


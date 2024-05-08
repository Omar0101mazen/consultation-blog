# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone
# from django.urls import reverse

# from django.core.validators import MinValueValidator, MaxValueValidator
# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)


#     def __str__(self):
#         return self.title

# class Rating(models.Model):
#     # حقل التقييم
#     rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
#     # علاقة ForeignKey مع نموذج المستخدم
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     # يمكنك إضافة حقول إضافية حسب احتياجاتك، مثل الكائن المقيم
    
#     def __str__(self):
#         return str(self.rating)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True,null=True)
    
    
    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)  # Save the post first to get a valid pk
        if not self.slug:  # Check if the slug is empty
            self.slug = slugify(self.pk)
            super(Post, self).save(*args, **kwargs) 
        
        
    def __str__(self) :
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20] 
    
    
class CommentRating(models.Model):
    RATING_CHOICES = (
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    )
    comment = models.ForeignKey(Comment, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f"{self.user.username} rated {self.rating}/5"
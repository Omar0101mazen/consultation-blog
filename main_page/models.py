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
    
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args, **kwargs)
        
        
    def __str__(self) :
        return self.title


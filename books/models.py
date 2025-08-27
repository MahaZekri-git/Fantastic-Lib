from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



LANGUAGE_CHOICES = ( 
    ("Not available", "Not available"), 
    ("Anglais", "Anglais"), 
    ("Français", "Français"), 
    ("Arabe", "Arabe"), 
    ("Italien", "Italien"), 
    ("Espagnole", "Espagnole"), 
    ("Allemand", "Allemand"),    
)
class Book(models.Model):
    BKCategory=models.ForeignKey('Category',on_delete=models.CASCADE, blank=True,null=True)
    BKTitle=models.CharField(max_length=100,verbose_name=_("book title")) 
    BKLanguage = models.CharField(max_length = 20, choices = LANGUAGE_CHOICES, default = 'Not available')   
    BKDescription=models.TextField(verbose_name=_("book description"))
    BKImage=models.ImageField(upload_to='book/',verbose_name=_("image"),blank=True,null=True)
    BKAuthor=models.ForeignKey('Author',on_delete=models.CASCADE, blank=True,null=True,related_name='books')
    BKFile=models.FileField(upload_to='book/', blank=True,null=True)
    
    BKSlug=models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.BKTitle

    def save(self,*args,**kwargs):
        if not self.BKSlug:
            self.BKSlug=slugify(self.BKTitle)
        super(Book,self).save(*args,**kwargs)    
            

class Category(models.Model):
    CATName=models.CharField(max_length=50, verbose_name=_("category name"))     
    CATParent=models.ForeignKey('self',limit_choices_to={'CATParent__isnull':True} , on_delete=models.CASCADE,null=True,blank=True, verbose_name=_("Main category"))
    CATDesc=models.TextField(verbose_name=_("category description"))
    CATImg=models.ImageField(upload_to='book/', verbose_name=_("category image"))

    def __str__(self):
        return str(self.CATName)
    
class Author(models.Model):
    ATName=models.CharField(max_length=50,unique=True, verbose_name=_("Author name"))     
    ATDesc=models.TextField(verbose_name=_("Author description"),null=True, blank=True)
    ATImg=models.ImageField(upload_to='book/', verbose_name=_("author image"),null=True, blank=True)
    ATOrigin=models.CharField(max_length=50, verbose_name=_("Origin"),null=True, blank=True) 
    ATLanguage= models.CharField(max_length = 20, choices = LANGUAGE_CHOICES, default = 'Arabe')
    
    ATSlug=models.SlugField(null=True, blank=True)

    def save(self,*args,**kwargs):
        if not self.ATSlug:
            self.ATSlug=slugify(self.ATName)
        super(Author,self).save(*args,**kwargs)

    def __str__(self):
        return str(self.ATName)
    

class UserManager(models.Manager):
        def basic_validator(self, postData):
            errors = {}
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')    
            if len(postData['name']) < 3:                
                errors["name"] = "Name should be at least 3 characters"
            if not EMAIL_REGEX.match(postData['email']):                
                errors["email"] = "Invalid email address"
            if len(postData['password']) < 8:                
                errors["password"] ="Password must be at least 8 characters."
            if postData['password'] != postData['confirmpassword']:                
                errors["confirmpassword"]="Passwords do not match!"
            return errors        
            

class User(models.Model):    
    USName=models.CharField(max_length=100,verbose_name=_("username"))
    USEmail=models.EmailField(verbose_name=_("accessories"))
    USImage=models.ImageField(upload_to='book/', verbose_name=_("user image"),null=True, blank=True)
    USPassword=models.CharField(max_length=50)
    objects = UserManager()

    def __str__(self):
        return str(self.USName)
    
class Testimonial(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='testimonial')
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='testimonial')
    content = models.TextField()

   



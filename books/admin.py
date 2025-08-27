from django.contrib import admin

from .models import Book,Category,Author, User, Testimonial

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(User)
admin.site.register(Testimonial)

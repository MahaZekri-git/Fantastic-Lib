from django.shortcuts import render, redirect
from .models import Book, Author, User, Testimonial
import mimetypes
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import get_object_or_404
import bcrypt



def signin_page(request):
    if 'user_id' in request.session:
        return redirect('/books/book_list')
    else:    
        if request.method=='POST':
            errors={}
            user = User.objects.filter(USEmail=request.POST['email'])
            if user:
                logged_user = user[0]                        
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.USPassword.encode()):
                    request.session['user_id'] = logged_user.id
                    return redirect('/books/book_list')
                else:
                    errors['password']="Mot de passe incorrecte" 
                    for key, value in errors.items():
                        messages.error(request, value)
                    return redirect("/books/signin")    
            else:
                errors['email']="Email does not exist" 
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect("/books/signin")
    return render(request,'books/signin.html')   



def index(request):
    if 'user_id' in request.session:    
        context={'user': User.objects.get(id=request.session['user_id'])}
    else:
        context={}
    
    return render(request,'books/index.html',context=context)


    

def signup_page(request): 
    if request.method=='POST':
        errors = User.objects.basic_validator(request.POST)        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books/signup')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user=User.objects.create(USName=request.POST['name'],USEmail=request.POST['email'],USPassword=pw_hash)
            messages.success(request, "User successfully added") 
            request.session['user_id'] = user.id                
            return redirect('/books/book_list')
    return render(request,'books/signup.html')    

def contact_page(request):
    if 'user_id' in request.session:    
        context={'user': User.objects.get(id=request.session['user_id'])}
    else:
        context={}

    return render(request,'books/contact.html', context=context)

def category_page(request):
    if 'user_id' in request.session:    
        context={'user': User.objects.get(id=request.session['user_id'])}
    else:
        context={}
    return render(request,'books/categories.html',context=context)

def about_page(request):
    if 'user_id' in request.session:    
        context={'user': User.objects.get(id=request.session['user_id'])}
    else:
        context={}
    return render(request,'books/about.html',context=context)

def book_list(request):
   
    if 'user_id' in request.session:
        print(request.session['user_id'])
        book_list=Book.objects.all()
        paginator = Paginator(book_list, 8)
        page_number = request.GET.get("page")
        book_list = paginator.get_page(page_number)   
        context={'book_list':book_list, 'user': User.objects.get(id=request.session['user_id'])}            
        return render(request,'books/book_list.html',context=context)
    return redirect("/books/")


def book_detail(request,slug):
    if 'user_id' in request.session:    
        book=Book.objects.get(BKSlug=slug) 
        user = User.objects.get(id=request.session['user_id']) 
        
        testimonials=Testimonial.objects.filter(book=book) 
        existing_testimonial = Testimonial.objects.filter(user=user, book=book).first()
        if testimonials:    
            context={
                'book':book, 'user': user,'testimonials':testimonials,'existing_testimonial': existing_testimonial
            }
        else:
            context ={
                'book':book, 'user': user,'existing_testimonial': existing_testimonial
            }   
        if request.method == 'POST':
            content = request.POST.get('content')           
            Testimonial.objects.create(user=user, book=book, content=content)
            return redirect('/books/'+slug)
        else:
            return render(request,'books/book_detail.html',context=context)
    return redirect("/books/")

def author_list(request):
    if 'user_id' in request.session:   
        author_list=Author.objects.all()
        paginator = Paginator(author_list, 8)
        page_number = request.GET.get("page")
        author_list = paginator.get_page(page_number)
        context={'author_list':author_list, 'user': User.objects.get(id=request.session['user_id'])
             
    }
        return render(request,'books/author_list.html',context)
    return redirect("/books/")


def author_detail(request,slug):
    user_id=request.session['user_id']
    if user_id:
        author=Author.objects.get(ATSlug=slug)
        context={
            'author':author, 'user': User.objects.get(id=user_id)
        }
        return render(request,'books/author_detail.html',context=context)
    return redirect("/books/")


def author_book_list(request,slug):
    user_id=request.session.get('user_id')
    if user_id:
        this_author=Author.objects.get(ATSlug=slug)
        books=Book.objects.filter(BKAuthor=this_author)
        paginator = Paginator(books, 8)
        page_number = request.GET.get("page")
        books = paginator.get_page(page_number)    
        context={
            'author':this_author,
            'books':books, 'user': User.objects.get(id=user_id)
            
        }
        return render(request,'books/author_book_list.html',context=context)
    return redirect("/books/")

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/books/')


def DownloadBook(request,slug):    
    book = get_object_or_404(Book, BKSlug=slug)
    file_path = book.BKFile.path

    # Get the file's MIME type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'  # Default MIME type

    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = content_type
    response['Content-Disposition'] = f'attachment; filename="{book.BKTitle}{file_path[-4:]}"'
    return response

def delete_testimonial(request,slug):
    if 'user_id' in request.session:
        book=Book.objects.get(BKSlug=slug)
        user=User.objects.get(id=request.session['user_id'])
        testimonial=Testimonial.objects.get(book=book,user=user)
        testimonial.delete()
    return redirect('/books/'+ slug)
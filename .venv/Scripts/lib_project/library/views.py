from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book,Appeals
from .forms import BookForm,RegistrationForm,SearchBook
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.
# def testfunc(request):
#     books = Book.objects.all()
#     for book in books:
#         print(book.author+" "+book.nameofbook)
#
#     return HttpResponse("Hello!!!")

def start(request):
    log="login"
    log_url="/login"
    if  request.user.is_authenticated:
        log="logout"
        log_url="/logout"
    return render(request,"start_page.html",{"log":log,"log_url":log_url})


#@login_required(login_url='/login/')
def all_books(request):
    books = None
    if request.method == "POST":
        #form = Book(request.POST, request.FILES)
        #print(form['nameofbook'])
        nameofbook = request.POST.get("nameofbook")
        author =  request.POST.get("author")
        genre = request.POST.get("genre")
        if nameofbook!='' and author!='' and genre!='':
             books = Book.objects.filter(nameofbook__icontains=nameofbook, author__icontains=author
                                        ,genre__icontains = genre)
        if nameofbook=='' and author!='' and genre!='':
             books = Book.objects.filter(author__icontains=author
                                        ,genre__icontains = genre)
        if nameofbook!='' and author=='' and genre=='':
             books = Book.objects.filter(nameofbook__icontains=nameofbook)
        if nameofbook=='' and author!='' and genre=='':
             books = Book.objects.filter(author__icontains=author)

        if nameofbook == '' and author == '' and genre != '':
             books = Book.objects.filter(genre__icontains=genre)
        if nameofbook != '' and author != '' and genre == '':
             books = Book.objects.filter(nameofbook__icontains = nameofbook, author__icontains = author)
        if nameofbook != '' and author == '' and genre != '':
             books = Book.objects.filter(nameofbook__icontains=nameofbook, genre__icontains=genre)

# Сделать варианты (sdelano)

    else:
        books = Book.objects.all()
    search_form = SearchBook()

    #передаем на клиент динамический шаблон
    return render(request, "all_books.html", {"search_form":search_form,"books": books,"login":request.user.is_authenticated})

@login_required(login_url='/login/')
def order(request):
    if request.method == "POST":
        books_id = request.POST.getlist("book_id");#list of book id
        if "order_books" in request.session:
            current_ids =  request.session["order_books"]
            for id in books_id:
                if (id in current_ids)==False:
                    current_ids.append(id)
            #keep order in session
        request.session["order_books"] = books_id
    #передаем на клиент динамический шаблон
    #get from session
    books=None
    if "order_books" in request.session:
        books_ids = request.session["order_books"]
        books = Book.objects.filter(book_id__in=books_ids)
    return render(request, "order_books.html", {"books": books})
@login_required(login_url='/login/')
def delete_from_order(request):
    book_id = request.POST['book_id']
    books_ids = request.session["order_books"]
    print(books_ids)
    print(book_id)
    books_ids.remove(book_id)
    print(books_ids)
    request.session["order_books"] = books_ids
    return redirect('/order/')
@login_required(login_url='/login/')
def clear_order(request):
    del request.session['order_books']
    return redirect('/order/')

@login_required(login_url='/login/')
def confirm_order(request):
    message = ''
    if "order_books" in request.session:
        books_ids = request.session["order_books"]
        books = Book.objects.filter(book_id__in=books_ids)
        user = request.user
        count = 0
        for book in books:
            if len(Appeals.objects.filter(reader=request.user,book=book)) == 0:
                appeal = Appeals(book = book,reader = user,issuedate = date.today() )
                appeal.save()
                count+=1
        message = 'Order successfull. You ordered '+str(count)+' books'
    else:
        message = 'You have not books for order'
    return render(request, "order_confirm.html", {"message": message})
@login_required(login_url='/login/')
def show_cabinet(request):
    username = request.user.first_name+' '+request.user.last_name
    appeals =  Appeals.objects.filter(reader=request.user)
    books = list(map(lambda appeal:{"book_id":appeal.book.book_id,
                                    "author":appeal.book.author,
                                    "nameofbook":appeal.book.nameofbook,
                                    "issuedate":str(appeal.issuedate),
                                    "dateofreturn":str(appeal.dateofreturn)
                                    },appeals))
    log = "login"
    log_url = "/login"
    if request.user.is_authenticated:
        log = "logout"
        log_url = "/logout"
    return render(request, "cabinet.html", {"username": username, "books":books,"log": log, "log_url": log_url})


# def create_book(request):
#     if request.method == "GET":
#          form = BookForm()
#          return render(request, "create_book.html", {"form": form})
#     if request.method == "POST":
#         form = BookForm(request.POST,request.FILES)  # получаем из запроса информацию о новой книге
#         #if form.is_valid():
#         form.save()#сохранение книги в базу
#         return redirect("/books")


def registration(request):
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST.get("email"),
                                        email=request.POST.get("email"),
                                        first_name=request.POST.get("first_name"),
                                        last_name=request.POST.get("last_name"),
                                        password=request.POST.get("password1"))
        user.save()
        #registration_form = RegistrationForm(request.POST)
        #registration_form.save()
        return redirect('/login/')
    form = RegistrationForm()
    return render(request,"registration.html",{"form":form})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url="/cabinet/"
            if request.POST['redirect'] != 'None':
                redirect_url = request.POST['redirect']
            return redirect(redirect_url)
    form = AuthenticationForm()
    redirect_page = request.GET.get('next')
    return render(request,"login.html",{"form":form,"redirect":redirect_page})
def user_logout(request):
    logout(request)
    return redirect('/home/')
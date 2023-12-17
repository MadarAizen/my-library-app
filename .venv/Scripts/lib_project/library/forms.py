from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['nameofbook', 'author', 'genre','collateralprice','rentalprice']

class RegistrationForm(UserCreationForm):
    #email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("first_name","last_name","email", "password1", "password2")
class SearchBook(ModelForm):
    class Meta:
        model = Book
        fields = ['nameofbook', 'author', 'genre']
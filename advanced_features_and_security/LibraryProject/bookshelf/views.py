from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request): return HttpResponse("Welcome to my bookshelf.)

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import Book
from .models import Library
from .models import UserProfile
from django.contrib.auth import login, logout
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required


# Create your views here.


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})


def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')                                        

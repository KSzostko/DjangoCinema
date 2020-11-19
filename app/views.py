from django.shortcuts import render, redirect
from django.views import generic
from .models import Movies, Seances, Discounts
from .forms import UserForm

# Create your views here.


def index(request):
    seances = Seances.objects.all()
    context = {'seances': seances}
    return render(request, 'app/index.html', context=context)


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            worker = form.save(commit=False)
            worker.phone_number = form.cleaned_data['phone_number']
            worker.name = form.cleaned_data['name']
            worker.surname = form.cleaned_data['surname']
            worker.position = form.cleaned_data['position']
            int_salary = int(form.cleaned_data['salary'])
            worker.salary = int_salary
            worker.save()

            return redirect('login')
    else:
        form = UserForm()

    return render(request, 'app/signup.html', context={'form': form})


class SeanceDetailView(generic.DetailView):
    model = Seances
    template_name = 'app/seance_detail.html'


class MovieDetailView(generic.DetailView):
    model = Movies
    template_name = 'app/movie_detail.html'


class DiscountsListView(generic.ListView):
    model = Discounts
    template_name = 'app/discounts_list.html'
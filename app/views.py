from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Movies, Seances, Discounts, Clients, Seats, Tickets
from . import forms


def index(request):
    seances = Seances.objects.all()
    context = {'seances': seances}
    return render(request, 'app/index.html', context=context)


def buy_ticket(request, pk):
    seance = get_object_or_404(Seances, pk=pk)

    if request.method == 'POST':
        form = forms.BuyTicketForm(request.POST)

        print("no siema siema")
        if form.is_valid():
            # creating user
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            phone = form.cleaned_data['phone']
            client = Clients(name=name, surname=surname, phone_number=phone)
            client.save()

            # getting seat
            # miejsce powinno juz byc raczej wczesniej przez admina do bazy dodane, wiec tutaj tylko wyszukujemy je
            nr_row = form.cleaned_data['row']
            print(type(nr_row))
            nr_seat = form.cleaned_data['seat']
            seat = get_object_or_404(Seats, room=seance.room, nr_row=nr_row, nr_seat=nr_seat)

            # creating ticket
            # TODO: doaj znizki do biletu
            # random discount for testing now
            discount = Discounts.objects.get(pk=1)
            constant_price = 30 #ustalona z gory cena
            # 
            ticket = Tickets(seance=seance, seat=seat, client=client, discount=discount, price=constant_price)
            ticket.save()

            return redirect('index')
    else:
        form = forms.BuyTicketForm()
    return render(request, 'app/buy_ticket.html', context={'form': form})


def create_user(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)

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
        form = forms.UserForm()

    return render(request, 'app/signup.html', context={'form': form})


def create_genre(request):
    if request.method == 'POST':
        form = forms.GenreForm(request.POST)

        if form.is_valid():
            genre = form.save()

            return redirect('index')
    else:
        form = forms.GenreForm()

    return render(request, 'app/genre_form.html', context={'form': form})


def create_movie(request):
    if request.method == 'POST':
        form = forms.MovieForm(request.POST)

        if form.is_valid():
            movie = form.save()

            return redirect('index')
    else:
        form = forms.MovieForm()

    return render(request, 'app/movie_form.html', context={'form': form})


def create_discount(request):
    if request.method == 'POST':
        form = forms.DiscountForm(request.POST)

        if form.is_valid():
            discount = form.save()

            return redirect('discounts_list')
    else:
        form = forms.DiscountForm()

    return render(request, 'app/discount_form.html', context={'form': form})


def create_room(request):
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)

        if form.is_valid():
            room = form.save()

            return redirect('index')
    else:
        form = forms.RoomForm()

    return render(request, 'app/room_form.html', context={'form': form})


def create_seat(request):
    if request.method == 'POST':
        form = forms.SeatForm(request.POST)

        if form.is_valid():
            seat = form.save()

            return redirect('index')
    else:
        form = forms.SeatForm()

    return render(request, 'app/seat_form.html', context={'form': form})


def create_seance(request):
    if request.method == 'POST':
        form = forms.SeanceForm(request.POST)

        if form.is_valid():
            seance = form.save()

            return redirect('index')
    else:
        form = forms.SeanceForm()

    return render(request, 'app/seat_form.html', context={'form': form})


class SeanceDetailView(generic.DetailView):
    model = Seances
    template_name = 'app/seance_detail.html'


class MovieDetailView(generic.DetailView):
    model = Movies
    template_name = 'app/movie_detail.html'


class DiscountsListView(generic.ListView):
    model = Discounts
    template_name = 'app/discounts_list.html'

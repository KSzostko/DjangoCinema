from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from .models import Movies, Seances, Discounts, Clients, Seats, Tickets, Genres, Workers, Rooms
from django.contrib import messages
from . import forms


def select_add(request):
    return render(request, 'app/add_select.html')


def index(request):
    seances = Seances.objects.all()
    genres = Genres.objects.all()
    ticketid = ""
    context = {'seances': seances, 'genres': genres, 'ticketid': ticketid}
    return render(request, 'app/index.html', context=context)


def buy_ticket(request, pk):
    seance = get_object_or_404(Seances, pk=pk)

    # pobranie wszystkich zniżek 
    discounts = Discounts.objects.all()

    # trochę pokrętne ale robi robote
    # pobranie wszystkich miejsc jakie są na sali przypisanej do seansu 
    seance_room = Rooms.objects.get(id=seance.room_id)
    seats_all = Seats.objects.filter(room=seance_room)

    # pobranie wszystkich zajętych miejsc
    seance_tickets = Tickets.objects.filter(seance=seance)

    seats_output = []
    if seance_tickets:
        seats_taken = [ticket.seat for ticket in seance_tickets]

        # usunięcie z wszystkich biletów tych zajętych
        seats_output = []
        for seat in seats_all:
            if seat not in seats_taken:
                seats_output.append(seat)
    else:
        seats_output = seats_all

    if request.method == 'POST':  # przekazanie zniżek i wolnych biletow do formy
        form = forms.BuyTicketForm(discounts, seats_output, request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            phone = form.cleaned_data['phone']

            # sprawdzamy czy jest juz klient o takich danyc
            # jesli tak to nie ma potrzebny tworzyc nowego
            global client
            try:
                client = Clients.objects.get(name=name, surname=surname, phone_number=phone)
            except Clients.DoesNotExist:
                client = None

            # nie znaleziono takiego klienta, wiec tworzymy nowego
            if client is None:
                client = Clients(name=name, surname=surname, phone_number=phone)
                client.save()

            # widget zwraca string składający się z kilku cyfr, temu tak rozdzielone
            # rząd powiniem być zawsze jednocyfrowy, inaczej trzeba to zmienić
            nr_row = form.cleaned_data['seats'][0]
            nr_seat = form.cleaned_data['seats'][1:]

            seat = get_object_or_404(Seats, room=seance.room, nr_row=nr_row, nr_seat=nr_seat)

            # wybrana przez klienta zniżka
            temp = form.cleaned_data['discount']

            # wartość zniżki 
            discount = Discounts.objects.get(value=temp)

            # obliczanie zniżki 
            price = int(30 - (30 * float(discount.value / 100)))  # 30 to ustalona z gory cena

            ticket = Tickets(seance=seance, seat=seat, client=client, discount=discount, price=price)
            ticket.save()
           
            
            seances = Seances.objects.all()
            genres = Genres.objects.all()
            ticketid = str(ticket.pk)
            context = {'seances': seances, 'genres': genres, 'ticketid': ticketid}
            return render(request, 'app/index.html', context=context)

    else:  # przekazanie zniżek i wolnych biletow do formy
        form = forms.BuyTicketForm(discounts, seats_output)
    return render(request, 'app/buy_ticket.html', context={'form': form, 'discounts': discounts, 'seats': seats_output})


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

    return render(request, 'app/seance_form.html', context={'form': form})


class SeanceDetailView(generic.DetailView):
    model = Seances
    template_name = 'app/seance_detail.html'


class MovieDetailView(generic.DetailView):
    model = Movies
    template_name = 'app/movie_detail.html'


class DiscountsListView(generic.ListView):
    model = Discounts
    template_name = 'app/discounts_list.html'


class UpdateMovieView(generic.UpdateView):
    model = Movies
    form_class = forms.MovieForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('movie_detail', kwargs={'pk': self.kwargs.get('pk')})


def update_seance(request, pk):
    seance = get_object_or_404(Seances, pk=pk)
    workers = seance.workers_set.all()

    current_user = request.user
    can_edit = False

    # checking if current user is in workers_set assigned to this seance, only then he can modify seance fields
    for worker in workers:
        if worker.username == current_user.username:
            can_edit = True

    form = forms.SeanceForm(request.POST or None, instance=seance)

    if form.is_valid():
        form.save()
        return redirect('seance_detail', pk=pk)

    context = {'form': form, 'can_edit': can_edit}
    return render(request, 'app/seances_update_form.html', context)


class SearchSeancesView(generic.ListView):
    model = Seances
    template_name = 'app/search_result.html'

    def get_queryset(self):
        name = self.request.GET.get('name')
        age = int(self.request.GET.get('age'))
        date = self.request.GET.get('date')

        if date == '':
            return Seances.objects.filter(
                movie__title__icontains=name,
                movie__age_restriction__lte=age
            )
        else:
            return Seances.objects.filter(
                date__gte=date,
                movie__title__icontains=name,
                movie__age_restriction__lte=age
            )


def delete_ticket(request):
    global error
    error = ''
    if request.method == 'POST':
        form = forms.DeleteTicketForm(request.POST)

        if form.is_valid():
            ticket_number = form.cleaned_data['ticket_number']
            phone_number = form.cleaned_data['phone_number']

            try:
                ticket = Tickets.objects.get(pk=ticket_number)
            except Tickets.DoesNotExist:
                ticket = None

            # correct data - you can delete ticket
            # otherwise show some message
            if ticket is not None and ticket.client.phone_number == phone_number:
                ticket.delete()
            else:
                error = 'Nie udało się usunąc biletu, niepoprawne dane'
                return render(request, 'app/cancel_ticket.html', {'form': form, 'error': error})

            return redirect('index')
    else:
        form = forms.DeleteTicketForm()

    return render(request, 'app/cancel_ticket.html', {'form': form, 'error': error})

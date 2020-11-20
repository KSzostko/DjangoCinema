from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(),
         name='logout', kwargs={'next_page': '/'}),
    path('signup/', views.create_user, name='signup'),
    path('senace/<int:pk>/', views.SeanceDetailView.as_view(), name='seance_detail'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('discounts/', views.DiscountsListView.as_view(), name='discounts_list'),
    path('buy/ticket/<int:pk>', views.buy_ticket, name='buy_ticket'),
]

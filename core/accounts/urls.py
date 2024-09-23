from django.urls import path
from . import views



urlpatterns = [
    path('app/accounts/register', views.registerPage, name='register'),
    path('app/auth/login/', views.loginPage, name='login'),
    path('app/logout/', views.logoutPage, name='logout'),

    
    path('app/dashboard/', views.dashboardPage, name='dashboard'),

    path('app/pirepsflight/', views.pirepsflightPage, name='pirepsflight'),
    path('registrar_voo_auto/', views.pirepsflightAutoPage, name='pirepsflight_auto'),
    path('app/edit/pirepsflighteditePage/<int:pk>/', views.pirepsflighteditePage, name='pirepsflighteditePage'),
    path('app/delete/pirepsflightdeletePage/<int:pk>/', views.pirepsflightdeletePage, name='pirepsflightdeletePage'), 

    
    path('app/flights/', views.flightsPage, name='flights'),
    path('app/pirepsflightAutoPage/', views.pirepsflightAutoPage, name='pirepsflightsAuto'),
    

    path('app/briefing/<str:pk>', views.briefingPage, name='briefing'),

    path('app/dadosvoos/<str:pk>', views.dadosvoosPage, name='voos'),
    path('app/eventos/', views.eventosPage, name='eventos'),
    path('app/eventos/agendamentos/<str:pk>', views.agendamentosPage, name='agendamentos'),
    path('app/eventos/seusagendamentos', views.seusagedamentosPage, name='seusagendamentos'),
    path('excluir_agendamento/<int:pk>/', views.excluir_agendamento, name='excluir_agendamento'),
    path('app/awards/', views.awards_view, name='awards'),
    path('app/awards/<int:award_id>/', views.award_detail_view, name='award_detail'),
    path('app/pilot/award_view/', views.pilotAwards_view, name='award_view'),
    path('app/list_award/', views.list_award, name='list_award'),
    
    
    path('app/radarflight/', views.radarflightPage, name='radarflight'),
    path('app/timeflight/', views.timeflight, name='timeflight'),
    path('app/user_details/<int:user_id>/', views.user_details, name='user_details'),
    
]
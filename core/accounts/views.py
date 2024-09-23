from datetime import timedelta, date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query_utils import Q

from accounts.forms import RegisterForm, PirepsFlightForm, AgendamentoForm
from .models import PirepsFlight, User, Evento, Agendamento, UserAward, PilotAward, Award
from accounts.requestsAPI import get_user_status, getUserFlights, bandeirasPaises, get_api_metar
from django.utils import timezone

from .generationevent import scrape_data  # Importe a função scrape_data do seu arquivo scraper.py

import os
import json
from django.conf import settings
   
# Obtém o número de voos dos últimos 30 dias para um usuário específico
def get_last_30_days_flight_count(user):
    # Calcula a data de 30 dias atrás a partir de hoje
    thirty_days_ago = date.today() - timedelta(days=30)

    # Filtra os voos aprovados nos últimos 30 dias
    approved_flights_last_30_days = PirepsFlight.objects.filter(
        pilot=user,
        status='Aprovado',
        registration_date__gte=thirty_days_ago
    )

    # Cria um dicionário para armazenar a contagem de voos por dia
    flights_per_day = {}

    # Itera sobre os voos aprovados nos últimos 30 dias
    for flight in approved_flights_last_30_days:
        # Obtém a data do voo
        flight_date = flight.registration_date.date()

        # Incrementa a contagem de voos para a data correspondente
        flights_per_day[flight_date] = flights_per_day.get(flight_date, 0) + 1

    # Cria uma lista de contagens de voos por dia nos últimos 30 dias
    flight_counts = [flights_per_day.get(thirty_days_ago + timedelta(days=i), 0) for i in range(30)]

    return flight_counts


# Página para registro de novos usuários
def registerPage(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Conta criada com sucesso. Agora você pode fazer login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect('register')

    return render(request, 'accounts/registerPage.html', {'form': form})


# Página de login
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Email or password is incorrect')
            return redirect('login')
    return render(request, 'accounts/loginPage.html')


# Página de logout
def logoutPage(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')

@login_required(login_url='login')
def dashboardPage(request):   

    # Obtém todos os voos do usuário ordenados por data de registro
    pireps_flights = PirepsFlight.objects.filter(pilot=request.user).order_by('-registration_date')

    # Obtém todos os voos aprovados do usuário ordenados por data de registro
    approved_flights = pireps_flights.filter(status='Aprovado')

    # Calcula o total de voos aprovados
    total_approved_flights = approved_flights.count()

    # Calcula o total de horas de voos aprovados
    total_approved_hours = approved_flights.aggregate(total_hours=Sum('flight_duration'))['total_hours']

    # Obtém a data e hora atuais
    now = timezone.now()

    # Calcula a data e hora de 30 dias atrás a partir de agora
    thirty_days_ago = now - timedelta(days=30)

    # Obtém a contagem de voos aprovados por dia nos últimos 30 dias para o usuário logado
    approved_flights_count_last_30_days = (
        approved_flights
        .filter(registration_date__gte=thirty_days_ago, registration_date__lte=now)
        .annotate(day=TruncDay('registration_date'))
        .values('day')
        .annotate(o=Count('day'))
        .order_by('day')
    )

    dates = [flight['day'].strftime('%d-%m') for flight in approved_flights_count_last_30_days]
    counts = [flight['o'] for flight in approved_flights_count_last_30_days]

    # Certifique-se de que você está agrupando os dados corretamente.
    used_aircraft_count_last_30_days = (
        approved_flights
        .filter(registration_date__gte=thirty_days_ago, registration_date__lte=now)
        .values('aircraft')
        .annotate(count=Count('aircraft'))
        .order_by('aircraft')
    )

    aircraft_labels = [aircraft_data['aircraft'] for aircraft_data in used_aircraft_count_last_30_days]
    aircraft_counts = [aircraft_data['count'] for aircraft_data in used_aircraft_count_last_30_days]

    # Calcular a pontuação total de cada usuário
    users_scores = PirepsFlight.objects.filter(status='Aprovado').values('pilot').annotate(total_score=Sum('scores')).order_by('-total_score')[:5]

    # Adicionar os usuários e suas pontuações aos resultados
    top_5_users = [(User.objects.get(pk=score['pilot']), score['total_score']) for score in users_scores]
    
    # Calcular o total de voos de cada usuário
    users_flights_count = PirepsFlight.objects.filter(status='Aprovado').values('pilot').annotate(total_flights=Count('pilot')).order_by('-total_flights')[:5]

    # Adicionar os usuários e seus totais de voos aos resultados
    top_5_usersflights = [(User.objects.get(pk=flight_count['pilot']), flight_count['total_flights']) for flight_count in users_flights_count]

    # Calcular o total de horas de voo de cada usuário
    users_total_hours = PirepsFlight.objects.filter(status='Aprovado').values('pilot').annotate(total_hours=Sum('flight_duration')).order_by('-total_hours')[:5]

    # Adicionar os usuários e seus totais de horas de voo aos resultados
    top_5_userstime = [(User.objects.get(pk=hours['pilot']), hours['total_hours']) for hours in users_total_hours]

    # Pega o METAR do último aeroporto de destino
    last_flight = pireps_flights.first()  # Último voo do usuário
    metar = get_api_metar(last_flight.arrival_airport) if last_flight else "METAR não disponível"
    

    context = {
        'pireps_flights': pireps_flights,
        'total_approved_flights': total_approved_flights,
        'total_approved_hours': total_approved_hours,
        'flights_count_per_day_last_30_days': approved_flights_count_last_30_days,
        'dates': dates,
        'counts': counts,
        'aircraft_labels': aircraft_labels,
        'aircraft_counts': aircraft_counts,
        'top_5_users': top_5_users,
        'top_5_usersfliths': top_5_usersflights,
        'top_5_userstime': top_5_userstime,
        'metar': metar,
    }

    return render(request, 'accounts/dashboardPage.html', context)

# Página para registro de voos
@login_required(login_url='login')
def pirepsflightPage(request):
    
    if request.method == 'POST':
        form = PirepsFlightForm(request.POST)
        if form.is_valid():
            pireps_flight = form.save(commit=False)
            pireps_flight.pilot = request.user  # Associa o usuário atual ao campo 'pilot'
            pireps_flight.save()
            messages.success(request, 'Parabens seu voo foi registrado')
            return redirect('pirepsflight')  # Redireciona para alguma view de sucesso após o registro
        else:
            messages.error(request, 'Ocorreu um erro ao registrar seu voo')
    else:
        form = PirepsFlightForm()
       
    return render(request, 'accounts/pirepsflightsPage.html', {'form': form})


# Página para edição de voos
@login_required(login_url='login')
def pirepsflighteditePage(request, pk):
    # Obtém o objeto PirepsFlight pelo ID (primary key)
    pireps_flight = get_object_or_404(PirepsFlight, id=pk)

    # Instancia o formulário com os dados do objeto obtido
    form = PirepsFlightForm(instance=pireps_flight)

    if request.method == 'POST':
        # Popula o formulário com os dados do POST
        form = PirepsFlightForm(request.POST, instance=pireps_flight)
        if form.is_valid():
            # Salva o formulário se for válido
            pireps_flight = form.save(commit=False)
            pireps_flight.pilot = request.user  # Associa o usuário atual ao campo 'pilot'
            pireps_flight.save()
            messages.success(request, 'Seu voo foi registrado com sucesso.')
            return redirect('pirepsflight')  # Redireciona para a view de sucesso
        else:
            # Exibe mensagem de erro caso o formulário seja inválido
            messages.error(request, 'Ocorreu um erro ao registrar seu voo.')

    context = {'form': form}
    return render(request, 'accounts/pirepsflightseditPage.html', context)


# Página para exclusão de voos
@login_required(login_url='login')
def pirepsflightdeletePage(request, pk):
    # Obtém o objeto PirepsFlight pelo ID (primary key)
    pireps_flight = PirepsFlight.objects.get(id=pk)
    pireps_flight.delete()
    return redirect('flights')  # Redireciona para a view de sucesso
    


@login_required(login_url='login')    
def pirepsflightAutoPage(request):
    # Obtém o perfil do usuário logado
    user_profile = request.user.profileIFC
    #print(user_profile)

    # Obtém o ID do usuário com base no perfil
    user_data = get_user_status(user_profile)
   
    
    user_id = user_data[0]['userId']
    #print(user_id)  # Isso irá imprimir o 'userId'


    flights_selection = getUserFlights(user_id)['data']
    #print(flights_selection)
   
    # Filtra os 5 últimos voos
    last_flights = flights_selection[:5]
    #print(last_flights)

    # Cria uma instância do formulário
    if request.method == 'POST':
        form = PirepsFlightForm(request.POST)
        if form.is_valid():
            pirep = form.save(commit=False)
            pirep.pilot = request.user  # Atribui o piloto (usuário logado)
            pirep.save()
            return redirect('pirepsflightsAuto')  # Redireciona após salvar
    else:
        form = PirepsFlightForm()  # Cria um formulário vazio para exibição

    # Define o contexto com os dados a serem passados para o template
    context = {
        'last_flights': last_flights,
        'form': form,  # Passa o formulário para o template
        'user_id': user_id,
    }
    
    # Renderiza a página HTML com o contexto
    return render(request, 'accounts/pirepsflightsAutoPage.html', context)



# Página para visualização do briefing de um voo
@login_required(login_url='login')
def briefingPage(request, pk):
   pireps_flight = PirepsFlight.objects.get(id=pk)
   context = {'pireps_flight': pireps_flight}
   return render(request, 'accounts/briefing.html', context)


# Página para exibir todos os voos
@login_required(login_url='login')
def flightsPage(request):
    pireps_flights = PirepsFlight.objects.filter(pilot=request.user).order_by('-registration_date')
    paginator = Paginator(pireps_flights, 10)  # 10 itens por página

    page_number = request.GET.get('page')
    try:
        pireps_flights = paginator.page(page_number)
    except PageNotAnInteger:
        pireps_flights = paginator.page(1)
    except EmptyPage:
        pireps_flights = paginator.page(paginator.num_pages)

    context = {'pireps_flights': pireps_flights}
    return render(request, 'accounts/flights.html', context)


# Página para obter dados de voos vindo do site flightaware
@login_required(login_url='login')
def dadosvoosPage(request, pk):
    # Recupere o evento com o ID fornecido
    evento = get_object_or_404(Evento, pk=pk)
    
    # Recupere os dados de voos paginados para o aeroporto do evento
    url = f'https://pt.flightaware.com/live/airport/{evento.aeroporto}'
    dados_voos = scrape_data(url, evento.tipo)

    # Obter todos os números de voos já registrados
    numeros_de_voos_registrados = Agendamento.objects.values_list('numero_voo', flat=True)

    # Configure a paginação dos dados de voos
    paginator = Paginator(dados_voos, 10)  # 10 itens por página
    page = request.GET.get('page')
    try:
        dados_voos_paginated = paginator.page(page)
    except PageNotAnInteger:
        # Se o número da página não for um número inteiro, retorne a primeira página
        dados_voos_paginated = paginator.page(1)
    except EmptyPage:
        # Se a página está fora do intervalo, retorne a última página de resultados
        dados_voos_paginated = paginator.page(paginator.num_pages)

    # Se o método de solicitação for POST, processar o formulário de agendamento
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            # Crie uma instância do agendamento com os dados do formulário
            agendamento = form.save(commit=False)
            # Associe o agendamento ao evento atual
            agendamento.evento = evento
            # Use a data do evento como data do agendamento, mesmo que a data do evento seja anterior à data atual.
            agendamento.data = evento.data
            # Use o aeroporto do evento como origem
            agendamento.origem = evento.aeroporto
            # Use a hora do evento como hora de partida do agendamento
            agendamento.hora_partida = evento.hora

             # Atribuindo o nome completo ao campo piloto do agendamento
            agendamento.piloto = request.user
            agendamento.save()
            messages.success(request, 'Parabens seu voo foi agendado')
            return redirect('seusagendamentos')
        else:
            messages.error(request, 'Ocorreu um erro ao registrar seu voo')
    else:
        # Se o método de solicitação não for POST, crie um formulário em branco
        form = AgendamentoForm()

    # Renderize a página com os dados de voos paginados, o evento e o formulário de agendamento
    context = {
        'dados_voos_paginated': dados_voos_paginated,
        'evento': evento,
        'form': form,
        'messages': messages.get_messages(request),  # Adicionando as mensagens à variável de contexto
        'numeros_de_voos_registrados': numeros_de_voos_registrados,
    }
    return render(request, 'accounts/voos.html', context)

@login_required(login_url='login')
def eventosPage(request):
    # Recupere todos os eventos do banco de dados
    eventos = Evento.objects.all().order_by('data', 'hora')

    # Passe os eventos para o contexto do render
    context = {'eventos': eventos}
    return render(request, 'accounts/eventosPage.html', context)

@login_required(login_url='login')
def agendamentosPage(request, pk):
    # Recupere o evento com o ID fornecido
    evento = get_object_or_404(Evento, pk=pk)
    
    # Recupere os agendamentos associados ao evento específico
    agendamentos = Agendamento.objects.filter(evento=evento)
    
    context = {
        'evento': evento,
        'agendamentos': agendamentos,
    }
    
    return render(request, 'accounts/agendamentosPage.html', context)

@login_required(login_url='login')
def seusagedamentosPage(request):
    agendamentos = Agendamento.objects.filter(piloto=request.user)

    context = {
        'agendamentos': agendamentos,
    }
    return render(request, 'accounts/seusagendamentosPage.html', context)

@login_required(login_url='login')
def excluir_agendamento(request, pk):

    agendamento  = Agendamento.objects.get(id=pk)
    agendamento.delete()
    return redirect('seusagendamentos')
    

@login_required(login_url='login')
def radarflightPage(request):
    return render(request, 'accounts/radarflightPage.html')

@login_required(login_url='login')
def awards_view(request):
    user = request.user
    user_awards = UserAward.objects.filter(user=user)
    flights = PirepsFlight.objects.filter(pilot=user, status='Aprovado')

    for user_award in user_awards:
        required_flights = list(user_award.award.flight_legs.all())
        allowed_icaos = [icao.company_icao for icao in user_award.award.allowed_icao.all()]
        allowed_aircrafts = [ac.aircraft for ac in user_award.award.allowed_aircrafts.all()]

        for required_flight in required_flights:
            required_flight.is_completed = False
            for flight in flights:
                # Verificar se o voo atende aos critérios dos aeroportos
                if flight.departure_airport == required_flight.from_airport and flight.arrival_airport == required_flight.to_airport:
                    # Se houver ICAOs permitidos, verificá-los, caso contrário, ignorar essa verificação
                    icao_check = not allowed_icaos or flight.flight_icao in allowed_icaos
                    # Se houver aeronaves permitidas, verificá-las, caso contrário, ignorar essa verificação
                    aircraft_check = not allowed_aircrafts or flight.aircraft in allowed_aircrafts

                    # Se ambas as verificações (quando aplicáveis) forem verdadeiras, marcar como completado
                    if icao_check and aircraft_check:
                        required_flight.is_completed = True
                        break

    context = {
        'user_awards': user_awards,
        'flights': flights,
    }
    return render(request, 'accounts/awardsPages.html', context)


@login_required(login_url='login')
def award_detail_view(request, award_id):
    user = request.user
    user_award = get_object_or_404(UserAward, id=award_id, user=user)
    flights = PirepsFlight.objects.filter(pilot=user, status='Aprovado')

    required_flights = list(user_award.award.flight_legs.all())
    allowed_icaos = [icao.company_icao for icao in user_award.award.allowed_icao.all()]
    allowed_aircrafts = [ac.aircraft for ac in user_award.award.allowed_aircrafts.all()]

    for required_flight in required_flights:
        required_flight.is_completed = False
        for flight in flights:
            # Verificar se o voo atende aos critérios dos aeroportos
            if flight.departure_airport == required_flight.from_airport and flight.arrival_airport == required_flight.to_airport:
                # Se houver ICAOs permitidos, verificá-los, caso contrário, ignorar essa verificação
                icao_check = not allowed_icaos or flight.flight_icao in allowed_icaos
                # Se houver aeronaves permitidas, verificá-las, caso contrário, ignorar essa verificação
                aircraft_check = not allowed_aircrafts or flight.aircraft in allowed_aircrafts

                # Se ambas as verificações (quando aplicáveis) forem verdadeiras, marcar como completado
                if icao_check and aircraft_check:
                    required_flight.is_completed = True
                    break

    context = {
        'user_award': user_award,
        'flights': flights,
        'required_flights': required_flights,
    }
    return render(request, 'accounts/awardDetail.html', context)



def pilotAwards_view(request):
    user = request.user
    user_awards = UserAward.objects.filter(user=user)

    context = {
        'user_awards': user_awards,
        
    }

    return render(request, 'accounts/pilotAwards.html', context)



def timeflight(request):
    # Carregar os dados das bandeiras dos países
    country_flags = bandeirasPaises()
    
    # Criar um dicionário para mapear o código do país à URL da bandeira
    flag_map = {item['pais']: item['bandeira'] for item in country_flags}

    users = User.objects.all()
    users_data = []
    for user in users:
        # Obtém todos os voos do usuário ordenados por data de registro
        pireps_flights = PirepsFlight.objects.filter(pilot=user).order_by('-registration_date')

        # Obtém todos os voos aprovados do usuário ordenados por data de registro
        approved_flights = pireps_flights.filter(status='Aprovado')

        # Calcula o total de voos aprovados
        total_approved_flights = approved_flights.count()

        # Calcula o total de horas de voos aprovados
        total_approved_duration = approved_flights.aggregate(
            total_duration=Sum('flight_duration')
        )['total_duration']

        # Calcular a pontuação total de cada usuário
        total_score = approved_flights.aggregate(
            total_score=Sum('scores')
        )['total_score'] or 0

        # Obter a URL da bandeira do país
        flag_url = flag_map.get(user.country, '')

        users_data.append({
            'user': user,
            'total_approved_flights': total_approved_flights,
            'total_approved_hours': total_approved_duration,
            'total_score': total_score,
            'flag_url': flag_url,
        })

    context = {
        'users_data': users_data,
    }
    return render(request, 'accounts/timeflight.html', context)



@login_required(login_url='login')
def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Busca o usuário com base no 
    get_user_if = get_user_status(user.profileIFC)[0]
    

    user_awards = UserAward.objects.filter(user=user)

    pilot_awards = PilotAward.objects.filter(participants=user) 
    
    pireps_flights = PirepsFlight.objects.filter(pilot=user, status='Aprovado')  # Mantém o filtro para o objeto user
    
    total_hours = pireps_flights.aggregate(total_hours=Sum('flight_duration'))['total_hours']
    
    total_flights = pireps_flights.count()
    
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    last_30_days_flights = pireps_flights.filter(registration_date__gte=thirty_days_ago).count()
    last_30_days_hours = pireps_flights.filter(registration_date__gte=thirty_days_ago).aggregate(total_hours=Sum('flight_duration'))['total_hours']
    
    context = {
        'user_details': user,
        'total_hours': total_hours,
        'total_flights': total_flights,
        'last_30_days_flights': last_30_days_flights,
        'last_30_days_hours': last_30_days_hours,
        'approved_flights': pireps_flights,  # Passa a lista de voos aprovados para o template
        'get_user_if': get_user_if,
        'user_awards': user_awards,
        'pilot_awards': pilot_awards  # Passa os PilotAwards para o template
    }

    return render(request, 'accounts/user_details.html', context)


def list_award(request):
    list_awards = Award.objects.all()

    context = {
        'list_awards': list_awards
    }
    return render(request, 'accounts/list_award.html', context)
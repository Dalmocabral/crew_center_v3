from datetime import timedelta, date


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
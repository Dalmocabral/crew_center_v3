from django.test import TestCase
from accounts.models import PirepsFlight, Award, UserAward, User, FlightLeg, AllowedAircraft, AllowedIcao

class AwardCompletionTest(TestCase):
    def setUp(self):
        # Criar um usuário de teste com os campos obrigatórios
        self.pilot = User.objects.create_user(
            email="pilot_test@example.com",
            password="password",
            first_name="Pilot",
            last_name="Test"
        )

        # Criar um Award (conquista)
        self.award = Award.objects.create(
            name="Conquista Azul",
            description="Voos Azul"
        )

        # Adicionar ICAOs permitidos ao Award
        AllowedIcao.objects.create(award=self.award, company_icao="AZU")  # ICAO da Azul

        # Adicionar uma perna de voo ao Award
        FlightLeg.objects.create(award=self.award, from_airport="SBGR", to_airport="SBRJ")

        # Adicionar aeronave permitida
        AllowedAircraft.objects.create(award=self.award, aircraft="A320")

        # Criar UserAward (conquista do usuário)
        self.user_award = UserAward.objects.create(user=self.pilot, award=self.award)

    def test_flight_completion_with_correct_icao(self):
        # Criar um voo com a companhia correta (AZU2365)
        flight = PirepsFlight.objects.create(
            flight_icao="AZU",  # ICAO correto da Azul
            flight_number="2365",
            departure_airport="SBGR",
            arrival_airport="SBRJ",
            aircraft="A320",
            pilot=self.pilot
        )

        # Verificar se a comparação funciona
        self.user_award.check_award_completion([flight])

        # Printar o progresso no terminal
        print(f"Progresso com ICAO correto: {self.user_award.progress}%")

        # O progresso deve ter aumentado porque o ICAO e os outros critérios estão corretos
        self.assertEqual(self.user_award.progress, 100)

    def test_flight_completion_with_incorrect_icao(self):
        # Criar um voo com a companhia errada (TAM2365)
        flight = PirepsFlight.objects.create(
            flight_icao="TAM",  # ICAO errado da TAM
            flight_number="2365",
            departure_airport="SBGR",
            arrival_airport="SBRJ",
            aircraft="A320",
            pilot=self.pilot
        )

        # Verificar se a comparação não valida o voo com ICAO incorreto
        self.user_award.check_award_completion([flight])

        # Printar o progresso no terminal
        print(f"Progresso com ICAO incorreto: {self.user_award.progress}%")
        
        # O progresso deve ser 0, pois o ICAO está errado
        self.assertEqual(self.user_award.progress, 0)

    def test_flight_completion_without_icao_restriction(self):
        # Criar um Award sem restrição de ICAO, apenas aeroportos
        award_no_icao = Award.objects.create(
            name="Conquista Aeroportos",
            description="Voos sem restrição de ICAO"
        )
        
        # Adicionar uma perna de voo ao Award (mesmo que o anterior)
        FlightLeg.objects.create(award=award_no_icao, from_airport="SBGR", to_airport="SBRJ")

        # Criar UserAward (conquista do usuário) sem restrição de ICAO
        user_award_no_icao = UserAward.objects.create(user=self.pilot, award=award_no_icao)

        # Criar um voo sem ICAO específico
        flight = PirepsFlight.objects.create(
            flight_icao="TAM",  # ICAO não deve importar
            flight_number="2365",
            departure_airport="SBGR",
            arrival_airport="SBRJ",
            aircraft="A320",
            pilot=self.pilot
        )

        # Verificar se a comparação funciona sem ICAO
        user_award_no_icao.check_award_completion([flight])

        # Printar o progresso no terminal
        print(f"Progresso sem restrição de ICAO: {user_award_no_icao.progress}%")

        # O progresso deve ser 100, pois apenas os aeroportos estão sendo validados
        self.assertEqual(user_award_no_icao.progress, 100)

    def test_flight_completion_without_aircraft_restriction(self):
        # Criar um Award sem restrição de aeronave, apenas ICAO e aeroportos
        award_no_aircraft = Award.objects.create(
            name="Conquista sem restrição de aeronave",
            description="Voos sem restrição de aeronave"
        )

        # Adicionar ICAO permitido ao Award
        AllowedIcao.objects.create(award=award_no_aircraft, company_icao="AZU")

        # Adicionar uma perna de voo ao Award
        FlightLeg.objects.create(award=award_no_aircraft, from_airport="SBGR", to_airport="SBRJ")

        # Criar UserAward (conquista do usuário) sem restrição de aeronave
        user_award_no_aircraft = UserAward.objects.create(user=self.pilot, award=award_no_aircraft)

        # Criar um voo sem restrição de aeronave
        flight = PirepsFlight.objects.create(
            flight_icao="AZU",
            flight_number="2365",
            departure_airport="SBGR",
            arrival_airport="SBRJ",
            aircraft="B737",  # Aeronave diferente, mas não importa
            pilot=self.pilot
        )

        # Verificar se a comparação funciona sem restrição de aeronave
        user_award_no_aircraft.check_award_completion([flight])

        # Printar o progresso no terminal
        print(f"Progresso sem restrição de aeronave: {user_award_no_aircraft.progress}%")

        # O progresso deve ser 100, pois apenas o ICAO e aeroportos estão sendo validados
        self.assertEqual(user_award_no_aircraft.progress, 100)

from django.contrib.auth.forms import UserCreationForm

from .models import User, PirepsFlight, Agendamento, Award
from django import forms


class RegisterForm(UserCreationForm):    

    def clean(self):
        cleaned_data = super().clean()

        for field_name, field_value in cleaned_data.items():
            if isinstance(field_value, str):
                # Converta a primeira letra para maiúscula para 'first_name' e 'last_name'
                if field_name in ['first_name', 'last_name']:
                    cleaned_data[field_name] = field_value.capitalize()

        return cleaned_data


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'profileIFC', 'base', 'grade', 'country']




# No início do seu arquivo ou em um arquivo importado


class PirepsFlightForm(forms.ModelForm):
    class Meta:
        model = PirepsFlight
        fields = ['event', 'flight_icao', 'flight_number', 'departure_airport', 'arrival_airport', 'alternate_airport', 'aircraft', 'flight_duration']
        labels = {
            'flight_icao': "Airline ICAO",
            'flight_number': 'Número do Voo',
            'departure_airport': 'Aeroporto de Partida',
            'arrival_airport': 'Aeroporto de Chegada',
            'alternate_airport': 'Aeroporto Alternativo',
            'aircraft': 'Aeronave',
            'flight_duration': 'Duração do Voo',
        }
        widgets = {
            'flight_icao': forms.TextInput(attrs={'placeholder': 'Example: ZZZ'}),
            'flight_number': forms.TextInput(attrs={'placeholder': 'Example: 0000'}),
            'departure_airport': forms.TextInput(attrs={'placeholder': 'Example: "SBGL" '}),
            'arrival_airport': forms.TextInput(attrs={'placeholder': 'Example: "SBSP" '}),
            'alternate_airport': forms.TextInput(attrs={'placeholder': 'Example: "SBGR" '}),
            'flight_duration': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()

        for field_name, field_value in cleaned_data.items():
            if isinstance(field_value, str):
                cleaned_data[field_name] = field_value.upper()

        return cleaned_data



class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['piloto', 'origem', 'destino', 'data', 'numero_voo', 'hora_partida', 'aeronave',]


        
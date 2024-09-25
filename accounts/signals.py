from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .models import PirepsFlight, UserAward, Award

@receiver(post_save, sender=PirepsFlight)
def check_awards(sender, instance, **kwargs):
    user = instance.pilot
    awards = Award.objects.all()
    
    for award in awards:
        user_award, created = UserAward.objects.get_or_create(user=user, award=award)
        if created:
            user_award.start_date = timezone.now()
            user_award.save()
        
        completed_flights = 0
        for required_flight in award.flight_legs.all():  # Corrigido para usar flight_legs
            for user_flight in PirepsFlight.objects.filter(pilot=user, status='Aprovado'):
                if (required_flight.from_airport == user_flight.departure_airport and
                    required_flight.to_airport == user_flight.arrival_airport and
                    user_flight.aircraft in [aircraft.aircraft for aircraft in award.allowed_aircrafts.all()]):
                    completed_flights += 1
                    break

        progress = (completed_flights / award.flight_legs.count()) * 100
        user_award.progress = progress
        if progress == 100 and not user_award.end_date:
            user_award.end_date = timezone.now()
        user_award.save()

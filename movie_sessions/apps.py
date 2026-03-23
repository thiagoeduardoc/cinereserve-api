from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta


class SessionsConfig(AppConfig):
    name = 'movie_sessions'
    
    def ready(self):
        """Inicializa APScheduler para limpar Reservations expiradas"""
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from .models import Reservation
            
            scheduler = BackgroundScheduler()
            
            def clean_expired_reservations():
                """Remove Reservations expiradas a cada minuto"""
                expired = Reservation.objects.filter(expires_at__lt=timezone.now())
                count = expired.count()
                if count > 0:
                    expired.delete()
                    print(f"[APScheduler] Deletadas {count} reservations expiradas")
            
            # Inicia o scheduler se não estiver rodando
            if not scheduler.running:
                scheduler.add_job(
                    clean_expired_reservations,
                    'interval',
                    minutes=1,
                    id='clean_expired_reservations',
                    replace_existing=True
                )
                scheduler.start()
                print("[APScheduler] Iniciado: limpeza de reservations expiradas a cada minuto")
        except Exception as e:
            print(f"[APScheduler] Erro ao inicializar: {e}")


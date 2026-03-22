# Generated migration for Reservation model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie_sessions', '0004_alter_session_room'),
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserved_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='room.seat')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='movie_sessions.session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-reserved_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('seat', 'session')},
        ),
    ]

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Verificar se superuser existe
if User.objects.filter(is_superuser=True).exists():
    print("✓ Superuser já existe")
else:
    # Criar superuser
    User.objects.create_superuser(username='admin', email='admin@test.com', password='admin123456')
    print("✓ Superuser 'admin' criado com sucesso")
    print("  Acesse: http://localhost:8000/admin/")
    print("  Username: admin")
    print("  Password: admin123456")

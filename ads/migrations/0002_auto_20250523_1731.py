from django.db import migrations
from django.utils.timezone import datetime

def add_initial_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Ad = apps.get_model('ads', 'Ad')
    ExchangeProposal = apps.get_model('ads', 'ExchangeProposal')

    user1 = User.objects.create(
        id=1,
        username='user1',
        email='egor.rodionovv@gmail.com',
        is_staff=True,
        is_active=True,
        is_superuser=True,
        password='pbkdf2_sha256$1000000$5TNfmfc4ZPZXJKmNx4mRsD$HQsnSIJWR1XpqymqYQeIidNx2n1YlKf8i+9wdgSS8L4=',
        last_login=datetime(2025, 5, 23, 14, 15, 47, 900440),
        date_joined=datetime(2025, 5, 23, 10, 21, 32, 979470)
    )
    user2 = User.objects.create(
        id=2,
        username='user2',
        email='test@gmail.com',
        is_staff=True,
        is_active=True,
        is_superuser=True,
        password='pbkdf2_sha256$1000000$W02OovxYsyD6LWi9KBJQZy$m9DJsI+6uyF7oc/uzbKc7SEQc/5ecUnmUi6MAe07irw=',
        last_login=datetime(2025, 5, 23, 14, 10, 31, 809337),
        date_joined=datetime(2025, 5, 23, 10, 59, 7, 598187)
    )

    ad1 = Ad.objects.create(
        id=6,
        user=user1,
        title='Карл Макрс "Капитал"',
        description='Хорошая книга, читать правда долго',
        image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Zentralbibliothek_Z%C3%BCrich_Das_Kapital_Marx_1867.jpg/330px-Zentralbibliothek_Z%C3%BCrich_Das_Kapital_Marx_1867.jpg',
        category='books',
        condition='good',
        created_at=datetime(2025, 5, 23, 14, 8, 14, 615233)
    )
    ad2 = Ad.objects.create(
        id=7,
        user=user1,
        title='Телефон',
        description='крутой, даже работает',
        image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Motorola_4050a-2.jpg/330px-Motorola_4050a-2.jpg',
        category='electronics',
        condition='used',
        created_at=datetime(2025, 5, 23, 14, 10, 7, 194338)
    )
    ad3 = Ad.objects.create(
        id=8,
        user=user2,
        title='Трусы со слоником',
        description='Носил единожды, больше не повторится',
        image_url='https://podarki-prikoly.com/image/cache/data/big/3a9_1-650x650.jpg',
        category='clothes',
        condition='good',
        created_at=datetime(2025, 5, 23, 14, 13, 24, 120836)
    )

    ExchangeProposal.objects.create(
        id=2,
        comment='Решил сменить приоритеты',
        status='accepted',
        created_at=datetime(2025, 5, 23, 14, 15, 4, 90060),
        ad_sender=ad1,
        ad_receiver=ad3
    )

    ExchangeProposal.objects.create(
        id=3,
        comment='надоела труба, хочу чего-то поинтереснее',
        status='pending',
        created_at=datetime(2025, 5, 23, 14, 18, 50, 521122),
        ad_sender=ad3,
        ad_receiver=ad2
    )

class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_data),
    ]
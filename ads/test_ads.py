from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal

class AdTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Description here',
            category='books',
            condition='new'
        )

    def test_ad_create(self):
        response = self.client.post(reverse('ad-create'), {
            'title': 'New Ad',
            'description': 'Some description',
            'category': 'electronics',
            'condition': 'good'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 2)

    def test_ad_edit(self):
        response = self.client.post(reverse('ad-edit', args=[self.ad.id]), {
            'title': 'Updated Ad',
            'description': 'Updated description',
            'category': 'books',
            'condition': 'used'
        })
        self.assertEqual(response.status_code, 302)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Ad')

    def test_ad_delete(self):
        response = self.client.post(reverse('ad-delete', args=[self.ad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(pk=self.ad.id).exists())

    def test_ad_search(self):
        response = self.client.get(reverse('ad-list') + '?search=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ad')

    def test_proposal_creation(self):
        receiver = User.objects.create_user(username='receiver', password='12345')
        ad2 = Ad.objects.create(
            user=receiver,
            title='Receiver Ad',
            description='Receiver description',
            category='books',
            condition='new'
        )
        response = self.client.post(reverse('proposal-create', args=[ad2.id]), {
            'ad_sender': self.ad.id,
            'ad_receiver': ad2.id,
            'comment': 'Would you like to trade?'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 1)
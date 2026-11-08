from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from .models import Device


class DeviceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.a=Device.objects.create(name="Фонд тканини",serial="V08-A")
        cls.b=Device.objects.create(name="Фонд дерево",serial="V08-B")
        cls.c=Device.objects.create(name="Вестибюль",serial="V08-C")

    def test_model_and_reverse(self):
        self.assertEqual(str(self.a),"Фонд тканини (V08-A)")
        self.assertEqual(reverse("monitoring:index"),"/")
        self.assertEqual(reverse("monitoring:detail",kwargs={"pk":7}),"/devices/7/")

    def test_index_and_detail(self):
        response=self.client.get(reverse("monitoring:index"))
        self.assertEqual(response.status_code,200)
        self.assertQuerySetEqual(response.context['devices'],[self.a,self.b,self.c])
        self.assertTemplateUsed(response,'monitoring/index.html')
        self.assertContains(self.client.get(reverse('monitoring:detail',args=[self.a.pk])),self.a.serial)

    def test_search_profile(self):
        before=list(Device.objects.values_list('name','serial'))
        response=self.client.get('/',{'q':'Фонд'})
        self.assertQuerySetEqual(response.context['devices'],[self.a,self.b])
        self.assertEqual(list(Device.objects.values_list('name','serial')),before)

    def test_empty_and_whitespace_query(self):
        for query in ('','   '):
            self.assertEqual(len(self.client.get('/',{'q':query}).context['devices']),3)

    def test_no_match_and_ukrainian(self):
        self.assertContains(self.client.get('/',{'q':'неіснуючий-зразок'}),'Пристроїв немає')
        self.assertQuerySetEqual(self.client.get('/',{'q':'ткан'}).context['devices'],[self.a])

    def test_empty_database(self):
        Device.objects.all().delete()
        self.assertContains(self.client.get('/'),'Пристроїв немає')

    def test_not_found(self):
        self.assertEqual(self.client.get('/devices/99999/').status_code,404)
        self.assertEqual(self.client.get('/devices/wrong/').status_code,404)

    def test_safe_methods(self):
        for url in ('/',reverse('monitoring:detail',args=[self.a.pk])):
            self.assertEqual(self.client.head(url).status_code,200)
            response=self.client.post(url)
            self.assertEqual(response.status_code,405)
            self.assertEqual(response.headers['Allow'],'GET, HEAD')

    def test_post_with_valid_csrf(self):
        client=Client(enforce_csrf_checks=True)
        client.get('/')
        token=client.cookies['csrftoken'].value
        self.assertEqual(client.post('/',HTTP_X_CSRFTOKEN=token).status_code,405)

    def test_unique_serial(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Device.objects.create(name='Дубль',serial='V08-A')
        self.assertEqual(Device.objects.count(),3)

    def test_validation_limits(self):
        for device in (Device(name='',serial='X'),Device(name='X'*81,serial='X'),
                       Device(name='X',serial='S'*41)):
            with self.assertRaises(ValidationError): device.full_clean()

    def test_escaping(self):
        device=Device.objects.create(name='<script>alert(1)</script>',serial='SAFE')
        response=self.client.get(reverse('monitoring:detail',args=[device.pk]))
        self.assertContains(response,'&lt;script&gt;')
        self.assertNotContains(response,'<script>')


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User=get_user_model()
        cls.admin=User.objects.create_superuser('test_admin',email='',password='test-only-password')
        cls.user=User.objects.create_user('test_user',password='test-only-password')
        cls.staff=User.objects.create_user('test_staff',password='test-only-password',is_staff=True)
        cls.device=Device.objects.create(name='Фонд тканини',serial='V08-A')

    def test_anonymous(self):
        self.assertEqual(self.client.get('/admin/').status_code,302)

    def test_regular_user(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get('/admin/').status_code,302)
        self.assertEqual(self.client.get('/admin/monitoring/device/').status_code,302)

    def test_staff_without_permissions(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get('/admin/').status_code,200)
        self.assertEqual(self.client.get('/admin/monitoring/device/').status_code,403)
        self.assertEqual(self.client.get('/admin/monitoring/device/add/').status_code,403)

    def test_superuser_admin(self):
        self.client.force_login(self.admin)
        response=self.client.get('/admin/monitoring/device/')
        self.assertContains(response,'V08-A')
        self.assertContains(response,'Фонд тканини')

    def test_admin_crud_and_duplicate(self):
        self.client.force_login(self.admin)
        add='/admin/monitoring/device/add/'
        self.assertEqual(self.client.post(add,{'name':'Фонд дерево','serial':'V08-B','_save':'1'}).status_code,302)
        response=self.client.post(add,{'name':'Дубль','serial':'V08-A','_save':'1'})
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.context['adminform'].form.errors.get('serial'))
        device=Device.objects.get(serial='V08-B')
        change=f'/admin/monitoring/device/{device.pk}/change/'
        self.assertEqual(self.client.post(change,{'name':'Фонд дерево оновлено','serial':'V08-B','_save':'1'}).status_code,302)
        device.refresh_from_db()
        self.assertEqual(device.name,'Фонд дерево оновлено')
        self.assertEqual(self.client.post(f'/admin/monitoring/device/{device.pk}/delete/',{'post':'yes'}).status_code,302)
        self.assertFalse(Device.objects.filter(pk=device.pk).exists())

    def test_admin_search(self):
        self.client.force_login(self.admin)
        self.assertContains(self.client.get('/admin/monitoring/device/',{'q':'V08-A'}),'Фонд тканини')

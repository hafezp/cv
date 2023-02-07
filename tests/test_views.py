
from django.test                    import Client, TestCase
from django.urls                    import reverse, resolve
from django.http                    import HttpRequest
from django.shortcuts               import render

from account.models                 import User


from income.models                  import Income
from income.views                   import home, CategoryCreateView



# class LoginTestCase(TestCase):

#     def test_url_available_by_name(self):                                                           
#         response = self.client.get(reverse("account:login"))
#         self.client.login(username='h@p.com', password='1')  
#         self.assertEqual(response.status_code, 200)


# class SamplePageEnterTestCase(TestCase):
#     ''' First of all need Logging in'''

#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='hafez',
#                                             phone_number='09353967479', 
#                                             email='lennon@thebeatles.com', 
#                                             password='1')


#     def test_entering_sample_page(self):                                                           
#         self.client.login(email='lennon@thebeatles.com', password='1')
#         response = self.client.get(reverse("income:incomelist"))
#         self.assertEqual(response.status_code, 200)


# class SamplePageTemplateNameTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='hafez',
#                                             phone_number='09353967479', 
#                                             email='hafez@paidary.com', 
#                                             password='1')


#     def test_template_name_correct(self):                                                           
#         self.client.login(email='hafez@paidary.com', password='1')
#         response = self.client.get(reverse("income:incomelist"))
#         self.assertTemplateUsed(response, "income/income_list.html")

  
# class ListViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='hafez',
#                                             phone_number='09353967479', 
#                                             email='hafez@paidary.com', 
#                                             password='1')

#         self.a = Income.objects.create(type='yes',select='in',price=10000)


#     def test_income_list_view(self):                                                          
#         self.client.login(email='hafez@paidary.com', password='1')
#         response = self.client.get(reverse("income:incomelist"))
#         self.assertEqual(response.status_code, 200)


# class HomePageUrlResolveTest(TestCase):

#     def test_home_url_resolves_view(self):
#         url = resolve(reverse('income:home'))
#         self.assertEqual(url.func, home)





from django.urls    import reverse
from django.test    import TestCase

from income.models  import Income


# Create your tests here.

# class IcomeModelTestCase(TestCase):


#     def create_income(self, type='yes', category='bank', select='in'):
#         return Income.objects.create(type=type, select=select, price=10000)

#     def test_income_creation(self):                                                                 # 1
#         a = self.create_income()
#         self.assertTrue(isinstance(a, Income))
#         self.assertEqual(a.__str__(), a.type)
#         #
#         objects = Income.objects.all()
#         self.assertEqual(objects.count(), 1)
#         first_saved_item = objects[0]
#         self.assertEqual(first_saved_item.type, 'yes')
















from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
# Create your tests here.
#Prueba unitaria
class ProfileTestCase(TestCase):
    def setUp(self):
        #Let's create an unser of testing
        User.objects.create_user('test','test@test.com','testqwerty12')
    #Allways the testing method has to strat with 'test_'
    def test_profile_exists(self):
        exixts = Profile.objects.filter(user__username='test').exists()
        #Execute the test case the variale exists has to be TRUE
        self.assertEqual(exixts,True)

        #To execute the test open the terminal and run:
        #python manage,py test registration


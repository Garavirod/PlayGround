from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Thread
# Create your tests here.

"""
    To especific class:
    run in terminal python manage.py test messenger.tests.TrheadTestCase
    
    To specific method inside of a class:
    run in terminal python manage.py test messenger.tests.TrheadTestCase.test_add_users_to_thread

"""
class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1',None,'qwerty1234')
        self.user2 = User.objects.create_user('user2',None,'qwerty1234')
        self.user3 = User.objects.create_user('user3',None,'qwerty1234')
        self.thread = Thread.objects.create()

    def test_add_users_to_thread(self):
        #this will add to relation Many to Many user1 and user2
        self.thread.users.add(self.user1,self.user2)
        self.assertEqual(len(self.thread.users.all()),2) #Est if there are two user into the thread
        
    #Recover an thread which  already exists through its users
    def test_filter_by_useres(self):
        self.thread.users.add(self.user1,self.user2)
        #All threads where is the user 1 and the user 2
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2) #Returns a list
        self.assertEqual(self.thread,threads[0])

    #Verify if there isn't a thread where the users doesn't take place in it        
    def test_filter_non_existent_thtrad(self):
        #All threads where is the user 1 and the user 2
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2) #Returns an empty list
        self.assertEqual(len(threads),0)

    def test_add_messages_to_thread(self):
        self.thread.users.add(self.user1,self.user2)
        message1  = Message.objects.create(user=self.user1,conent="I want to buy you somethng")
        message2  = Message.objects.create(user=self.user2,conent="There's nothing to be done")
        self.thread.messages.add(message1,message2)
        #Test how many messages are in the Thread
        self.assertEqual(len(self.thread.messages.all()),2)
        for message in self.thread.messages.all():
            print("User: {}, Message : {}".format(message.user,message.conent))

    #Testing an unser that doesn't take place in the thread
    def test_add_message_from_user_not_in_thread(self):
        self.thread.users.add(self.user1,self.user2)
        message1  = Message.objects.create(user=self.user1,conent="I want to buy you somethng")
        message2  = Message.objects.create(user=self.user2,conent="There's nothing to be done")
        message3  = Message.objects.create(user=self.user3,conent="I'm a spy")
        self.thread.messages.add(message1,message2,message3)
        # Para que el hilo solo acepte 2 mensajes, se crea una señal en el doc models.py
        self.assertEqual(len(self.thread.messages.all()),2)
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)#User who creates it
    conent = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class ThreadManager(models.Manager):
    def find(self,user1,user2):
        """
            La palabra recervada self hace referencias a las instancias
            de ese modelo en est caso Thread, ejemplo:

            self <=>  Thread.objects.all
        """
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset) > 0:
            return queryset[0]
        return None
    
    def find_or_create(self,user1,user2):
        #Buscamos is exite
        thread = self.find(user1,user2)
        # De lo contrari lo creamos
        if thread is None:
            # Creamos un hilo al cual añadimos al user 1 y 2
            thread = Thread.objects.create()
            thread.users.add(user1,user2)
        return thread

"""
    The thread is a place like a point (punto de encuentro)
    where the thread stores the users and the messages which 
    will be written by the useres

"""
class Thread(models.Model):
    users = models.ManyToManyField(User,related_name='threads') #user.threads all thread the user belong
    messages = models.ManyToManyField(Message)
    # Clase definida arriba, para crear nustros filtros personalizados
    objects = ThreadManager()
    # Campo de actualización
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

def messages_changed(sender,**kwargs):
    # Instancia que manda la señal, hilo al que intentamos añadir los mensajes
    instance = kwargs.pop('instance',None) #Saca la instancia, de no estar retornanr None
    # Acción que se está ejecutando, pre-add o post-add, en este caso el pre-add
    # momento justo anes de añadir los mensajes
    action = kwargs.pop('action',None)
    # Conjunto que alamcena los identificadores de todos los menasajes que se van a añadir a la ralcion many to many
    pk_set=kwargs.pop('pk_set',None)
    # Debugear
    print(instance,action,pk_set)

    """
        Tenemos que interceptar el pk_Set, buscar los mensajes que contiene 
        a partir de las pk y si su author no froma parte del hilo de comunicacion
        borrarlos para que o se añadan.
    """
    false_pk_set = set()
    if action is 'pre_add':
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            """
                 Si el autor del mensaje no esta dentro de los useres
                 que hay añadidos en la insancia del hilo
            """
            if msg.user not in instance.users.all():
                print("Oops! '{}', no forma parte del hilo!".format(msg.user))
                false_pk_set.add(msg_pk)
    pk_set.difference_update(false_pk_set)

    # Forzamos la actualización
    instance.save()
    
# Conecamos la señal con cualquier campo many to many de messages
m2m_changed.connect(messages_changed,sender=Thread.messages.through)

from gevent_fsm.fsm import State, transitions
import gevent
from . import messages
import random


class _Start(State):

    @transitions('Waiting')
    def start(self, controller):

        controller.changeState(Waiting)


Start = _Start()


class _Errored(State):

    @transitions('Waiting')
    def start(self, controller):

        controller.changeState(Waiting)


Errored = _Errored()


class _Waiting(State):

    def start(self, controller):
        if not controller.context.buffered_messages.empty():
            controller.context.queue.put(controller.context.buffered_messages.get())

    @transitions('Running')
    def onDeploy(self, controller, message_type, message):

        controller.changeState(Running)
        controller.context.deploy(message.data)



Waiting = _Waiting()


class _Running(State):


    @transitions('Completed')
    def onComplete(self, controller, message_type, message):

        controller.changeState(Completed)

    @transitions('Errored')
    def onError(self, controller, message_type, message):

        controller.changeState(Errored)


Running = _Running()


class _Completed(State):

    @transitions('Waiting')
    def start(self, controller):

        controller.changeState(Waiting)


Completed = _Completed()

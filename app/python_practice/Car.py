# -*- coding: utf-8 -*-

class Car(object):
    def __init__(self):...
    

    def start(self, command = 'engine start\n'):
        print(command)

    def stop(self, command = 'car stop\n'):
        print(command)

    def forward(self):
        print('Car is driving ...\n')

    def reverse(self):
        print('Car is reverse ...\n')


if __name__ == '__main__':
    car = Car()
    car.reverse()
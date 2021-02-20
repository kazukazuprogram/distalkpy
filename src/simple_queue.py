#!/usr/bin/env python3
# coding: utf-8

from threading import Thread


class NoArgs:
    pass


class AutoExecuteQueue:
    def __init__(self):
        self.queue = list()
        self.execute_thread = None

    def __execute(self):
        if len(self.queue) == 0:
            self.execute_thread = None
        else:
            t = Thread(target=self.queue[0][0], args=self.queue[0][1])
            t.start()
            t.join()
            del self.queue[0]
            self.__execute()

    def add(self, function, args=NoArgs()):
        self.queue.append([function, args])
        if self.execute_thread is None:
            self.execute_thread = Thread(target=self.__execute)
            self.execute_thread.start()

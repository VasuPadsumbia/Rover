from re import M
from Layers.L1_App.mqtt.mqtt_subscribe import MQTT_Subscribe
from queue import Queue
from app import AppCommand, Navigator, AppData, manoeuvre
from threading import Thread
class Worker:
    def __init__(self) -> None:
        self.appCommand = AppCommand()
        self.navigator = Navigator()
        self.MqttSub = MQTT_Subscribe()
        self.AppData = AppData()
        self.manouver = manoeuvre()

    def main(self):
        # Create the shared queue
        
        q1 = Queue()  # for app command
        q2 = Queue()  # for navigator target position
        t1 = Thread(target=self.appCommand.worker,args=(q1,q2,),)
        print("init thread 1")
        t2 = Thread(target=self.MqttSub.subscribe_mqtt, args=(q1,))
        print("init thread 2")
        t3 = Thread(target=self.AppData.worker)
        print("init thread 3")
        t4 = Thread(target=self.navigator.worker, args=(q2,))
        print("init thread 4")
        t5 = Thread(target=self.manouver.worker)
        print("init thread 5")
        t1.start()  
        print("thread 1 started")
        t2.start()
        print("thread 2 started")
        t3.start()
        print("thread 3 started")
        t4.start()
        print("thread 4 started")
        t5.start()
        print("thread 5 started")

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
if __name__ == "__main__":
    worker = Worker()
    worker.main()
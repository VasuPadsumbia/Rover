from calendar import c
from Layers.L1_App.mqtt.mqtt_subscribe import MQTT_Subscribe
from queue import Queue
from threading import Thread
from app import AppCommand
import pub_test as t

class Worker:
    def __init__(self) -> None:
        self.appCommand = AppCommand()
        self.MqttSub = MQTT_Subscribe()

    def main(self):
        # Create the shared queue and launch all threads
        q1 = Queue() # for app command
        q2 = Queue() # for navigator target position

        t1 = Thread(
            target=self.appCommand.worker,
            args=(
                q1,
                q2,
            ),
        )

        t2 = Thread(target=self.MqttSub.subscribe_mqtt, args=(q1,))
        t3 = Thread(target=t.test(), args=(q1,))

        t1.start()
        t2.start()
        t3.start()
        #t4.start()
        #t5.start()

        # Wait for all produced items to be consumed
        #t3.join()
        #q1.join()
        #q2.join()


if __name__ == "__main__":
    worker = Worker()
    worker.main()
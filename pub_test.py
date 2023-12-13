import time
from Layers.L2_Data.pub_data_handler import Pub_Handler

def test():
    publish = Pub_Handler()
    while True:
        msg_dict = {
                        "topic": '/bot/control',
                        "botCommand": 'forward',
                    }

        publish.data_handler(msg_dict)
        time.sleep(3)

        msg_dict = {
                        "topic": '/bot/control',
                        "manualMode": True,
                    }
        publish.data_handler(msg_dict)
        time.sleep(3)

        msg_dict = {
                        "topic": '/bot/control',
                        "autoMode": False,
                    }
        publish.data_handler(msg_dict)
        time.sleep(3)
        
        msg_dict = {
                        "topic": '/bot/control',
                        "targetLocation": (53.540966, 8.585301)
                    }
        publish.data_handler(msg_dict)
        time.sleep(3)
if __name__ == "__main__":
    test()
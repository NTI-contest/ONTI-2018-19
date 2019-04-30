import logging
import asyncio

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1, QOS_2

@asyncio.coroutine
def test_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://192.168.1.147/:1883')
    tasks = [
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_0')),
        asyncio.ensure_future(C.publish('Hi!!', b'TEST MESSAGE WITH QOS_1', 
            qos=QOS_1)),
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_2', 
            qos=QOS_2)),
    ]
    yield from asyncio.wait(tasks)
    logger.info("messages published")
    yield from C.disconnect()


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} \\
        %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(test_coro())
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()

    yield from C.connect('mqtt://192.168.1.147/:1883')

    yield from C.subscribe([
            ('/fromserver/car/#', QOS_2),
            ('/fromserver/drone/#', QOS_2),
            ('/fromserver/light/#', QOS_2)
         ])
    try:
        for i in range(1, 200):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            t = ''
            for a in packet.payload.data:
                t = t + str(bin(a))
            print("%d:  %s => %s" % (i, packet.variable_header.topic_name, t))
        yield from C.unsubscribe(['/fromserver/car/#', '/fromserver/drone/#', 
            '/fromserver/light/#'])
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(uptime_coro())
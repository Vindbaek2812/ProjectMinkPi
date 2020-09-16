import sys
import pika

# Set up the exchange environment
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Establish the exchange
channel.exchange_declare(exchange='sensor_exchange', exchange_type='topic')

# Establish a queue called
queue_name = sys.argv[1]
result = channel.queue_declare(queue=queue_name, exclusive=False)
queue_name = result.method.queue

binding_keys = sys.argv[1:]

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)


for binding_key in binding_keys:
    channel.queue_bind(
        exchange='sensor_exchange', queue=queue_name, routing_key=binding_key)

print(' [*] PiExchange is now running...')

from dotenv import load_dotenv
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.enums import PNStatusCategory
from pubnub.callbacks import SubscribeCallback
import os, time, uuid

load_dotenv()

class Listener(SubscribeCallback):
    def presence(self, pubnub, presence):
        print(f'\n-- Presence Event: {presence.event}')
        
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print(f'\n-- Successfully connected to PubNub!')
        elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            print(f'\n-- Disconnected from PubNub!')
        elif status.category == PNStatusCategory.PNConnectionError:
            print(f'\n-- Connection Error: {status.error_data.information}')
        else:
            print(f'\n-- Status Event: {status.category}')
        
    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel}')
        print(f'-- Message: {message_object.message}')

pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.getenv('PUBNUB_SUBSCRIBE_KEY')
pnconfig.publish_key = os.getenv('PUBNUB_PUBLISH_KEY')
pnconfig.uuid = str(uuid.uuid4())
pubnub = PubNub(pnconfig)
pubnub.add_listener(Listener())

TEST_CHANNEL = 'blockchain'

def main():
    try:
        print(f'Attempting to connect with UUID: {pnconfig.uuid}')
        print(f'Subscribe key: {pnconfig.subscribe_key[:8]}...')
        print(f'Publish key: {pnconfig.publish_key[:8]}...')
        
        pubnub.subscribe().channels([TEST_CHANNEL]).execute()
        print(f'Subscribed to channel: {TEST_CHANNEL}')
        
        time.sleep(2)  # Wait longer for connection to establish
        
        message = {
            'sender': pnconfig.uuid,
            'content': 'Hello PubNub!',
            'timestamp': time.time()
        }
        
        print('\nPublishing test message...')
        envelope = pubnub.publish().channel(TEST_CHANNEL).message(message).sync()
        
        if envelope.status.is_error():
            print(f'Error publishing message: {envelope.status.error_data.information}')
        else:
            print(f'Successfully published message! Timetoken: {envelope.result.timetoken}')
        
        print('\nListening for messages... Press Ctrl+C to exit')
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f'Error: {str(e)}')
    except KeyboardInterrupt:
        print('\nGracefully shutting down...')
        pubnub.unsubscribe().channels([TEST_CHANNEL]).execute()
        pubnub.stop()


if __name__ == '__main__':
  main()
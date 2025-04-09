## Environment Setup

1. Copy the environment template:

```bash
cp .env.template .env
```

2. Edit `.env` and replace the placeholder values with your actual PubNub credentials:

```
PUBNUB_SUBSCRIBE_KEY=your-actual-subscribe-key
PUBNUB_PUBLISH_KEY=your-actual-publish-key
```

**Activate the virtual environment**

```
source blockchain-env/bin/activate
```

**Install all packages**

```
pip3 install -r requirements.txt
```

**Run the tests**
Make sure to activate the virtual environment.

```
python3 -m pytest backend/tests
```

**Run the application and API**
Make sure to activate the virtual environment.

```
python3 -m backend.app
```

**Run a peer instance**
Make sure to activate the virtual environment.

```
export PEER=True && python3 -m backend.app
```

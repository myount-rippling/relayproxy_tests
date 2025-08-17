# /// script
# dependencies = [
#   "launchdarkly-server-sdk==9.11.1",
# ]
# ///
import time, logging
from ldclient import Context, LDClient
from ldclient.config import Config
import os

RELAY_PROXY_URI = "http://localhost:8030"

sdkKey = os.getenv("LD_ENV_DEVELOPMENT_SDK_KEY")
print("sdkKey: ", sdkKey)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(name)s:%(message)s")


def get_client():
    config = Config(
        sdkKey,
        application={"id": "failure-mode-test"},
        initial_reconnect_delay=1,
        poll_interval=30,
        base_uri=RELAY_PROXY_URI,
        stream_uri=RELAY_PROXY_URI,
        events_uri=RELAY_PROXY_URI,
    )


    client = LDClient(config=config, start_wait=15)

    if not client.is_initialized():
        print("ERROR: Client failed to initialize within timeout")
        exit(1)

    return client

def main():
    client = get_client()

    print("LaunchDarkly client initialized successfully!")
    context = Context.builder("user").set("key", "Sandy").build()

    while True:
        print("LDClient initialized:", client.is_initialized())
        print("feature-flag-name: ", client.variation("abhay-test-unreliable", context, "default"))
        time.sleep(1)

if __name__ == "__main__":
    main()

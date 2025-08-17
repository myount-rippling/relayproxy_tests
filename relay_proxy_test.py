# /// script
# dependencies = [
#   "launchdarkly-server-sdk==9.11.1",
# ]
# ///
import time, logging
from ldclient import Context, LDClient
from ldclient.config import Config
import os

LAUNCHDARKLY_BASE_URI="http://ld-relay-proxy:8030"
LAUNCHDARKLY_STREAM_URI = "http://ld-relay-proxy:8030"
# LAUNCHDARKLY_EVENTS_URI = "http://ld-relay-proxy:8030"
LAUNCHDARKLY_EVENTS_URI = "https://events.launchdarkly.com"

sdkKey = os.getenv("LD_ENV_DEVELOPMENT_SDK_KEY")
print("sdkKey: ", sdkKey)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(name)s:%(message)s")


def get_client():
    config = Config(
        sdkKey,
        application={"id": "failure-mode-test"},
        initial_reconnect_delay=1,
        poll_interval=30,
        base_uri=LAUNCHDARKLY_BASE_URI,
        stream_uri=LAUNCHDARKLY_STREAM_URI,
        events_uri=LAUNCHDARKLY_EVENTS_URI,
        enable_event_compression=True,
    )


    client = LDClient(config=config, start_wait=15)

    if not client.is_initialized():
        print("ERROR: Client failed to initialize within timeout")
        exit(1)

    return client

def main():
    client = get_client()

    print("LaunchDarkly client initialized successfully!")
    count = 0

    while True:
        count += 1
        context = Context.builder("user").set("key", f"Sandy-{count}").build()
        result = client.variation("myount-events-test", context, "default")
        print("feature-flag-name: ", result)
        time.sleep(1)

if __name__ == "__main__":
    main()

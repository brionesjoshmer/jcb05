import logging
import json
from typing import List
import azure.functions as func
from . import smtp_util


def main(events: List[func.EventHubEvent]):
    logging.info("+++++++++++ START ++++++++++")

    # Comment out this statement if notification by an email is required.
    return

    logging.info(events)
    for event in events:
        logging.info("##### event #####")
        event_json = json.loads(event.get_body().decode("utf-8"))
        logging.info(event_json)
        smtp_util.send_email(event_json)
        # try:
        #     smtp_util.send_email(event)
        # except Exception as e:
        #     logging.error("can not send message: %s", e.args)


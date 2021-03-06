#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import pytest
import connections
import random
import test_utilities
from environment import runtime_config
from adapters import print_message as log_message


@pytest.mark.testgroup_edgehub_module_client
@pytest.mark.testgroup_iothub_module_client
@pytest.mark.callsSendEvent
def test_module_send_event_to_iothub():

    log_message("connecting module client")
    module_client = connections.connect_test_module_client()
    log_message("connecting eventhub client")
    eventhub_client = connections.connect_eventhub_client()

    sent_message = test_utilities.random_string_in_json()
    log_message("sending event: " + str(sent_message))
    module_client.send_event(sent_message)

    log_message("wait for event to arrive at eventhub")
    received_message = eventhub_client.wait_for_next_event(
        runtime_config.test_module.device_id,
        test_utilities.default_eventhub_timeout,
        expected=sent_message,
    )
    if not received_message:
        log_message("Message not received")
        assert False

    log_message("disconnecting module client")
    module_client.disconnect()
    log_message("disconnecting eventhub client")
    eventhub_client.disconnect()

#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import pytest
import connections
import random
import time
import test_utilities
from adapters import print_message as log_message
import environment
import threading

output_name = "loopout"
input_name = "loopin"
receive_timeout = 60


@pytest.mark.testgroup_edgehub_module_client
@pytest.mark.callsendOutputMessage
@pytest.mark.receivesInputMessages
@pytest.mark.handlesLoopbackMessages
def test_module_input_output_loopback():
    log_message("connecting module client")
    module_client = connections.connect_test_module_client()
    log_message("enabling input messages")
    module_client.enable_input_messages()

    result_messages = [None] * 1
    expected_messages = [None] * 1
    sent_message = test_utilities.max_random_string()
    expected_messages[0] = sent_message

    if environment.language == "ppdirect":
        listen_thread = threading.Thread(target=wait_for_input_message, args=(
        10, module_client, input_name, environment.module_id, result_messages, expected_messages, 0, 1))
        listen_thread.daemon = True
        listen_thread.start()
    else:
        log_message("listening for input messages")
        input_thread = module_client.wait_for_input_event_async(input_name)

    log_message("sending output event: " + str(sent_message))
    module_client.send_output_event(output_name, sent_message)

    if environment.language == "ppdirect":
        listen_thread.join(10)

        received_message = result_messages[0]
        if not received_message:
            log_message("Message not received")
            assert False
    else:
        log_message("waiting for input message to arrive")
        received_message = input_thread.get(receive_timeout)
        assert received_message == sent_message

    log_message("Disconnecting clients")
    module_client.disconnect()


def wait_for_input_message(timeout, module_client, input_name, module_id, results, expected, index, capacity):
    """
    This method has been defined only for python direct SDK
    """
    log_message("ModuleAPI: waiting for input at {}".format(module_id))
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        received_input_message = module_client.wait_for_input_event_async(input_name)
        actual = str(received_input_message.data, "utf-8")
        log_message("The message received was " + actual)
        if expected[index] == actual:
            log_message("DeviceAPI: message received as expected")
            results[index] = actual
            if index == capacity:
                return
            index = index + 1
        else:
            log_message("ModuleAPI: unexpected message.  skipping")
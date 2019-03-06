#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import pytest
import connections
import random
import time
import test_utilities
import environment
from adapters import print_message as log_message
import threading

@pytest.fixture(scope="module", autouse=True)
def set_channels(request):
    global friend_to_test_output
    global test_to_friend_input
    friend_to_test_output = "to" + environment.module_id
    test_to_friend_input = "from" + environment.module_id


friend_to_test_output = None
friend_to_test_input = "fromFriend"

test_to_friend_output = "toFriend"
test_to_friend_input = None

receive_timeout = 60


@pytest.mark.testgroup_edgehub_module_client
@pytest.mark.callsSendOutputEvent
def test_module_to_friend_routing():

    test_client = connections.connect_test_module_client()
    friend_client = connections.connect_friend_module_client()
    friend_client.enable_input_messages()

    friend_input_thread = friend_client.wait_for_input_event_async(test_to_friend_input)

    sent_message = test_utilities.max_random_string()
    test_client.send_output_event(test_to_friend_output, sent_message)

    received_message = friend_input_thread.get(receive_timeout)
    assert received_message == sent_message

    friend_client.disconnect()
    test_client.disconnect()


@pytest.mark.testgroup_edgehub_module_client
@pytest.mark.receivesInputMessages
def test_friend_to_module_routing():

    test_client = connections.connect_test_module_client()
    test_client.enable_input_messages()
    friend_client = connections.connect_friend_module_client()

    result_messages = [None] * 1
    expected_messages = [None] * 1

    sent_message = test_utilities.max_random_string()
    expected_messages[0] = sent_message

    if environment.language == "ppdirect":
        listen_thread = threading.Thread(target=wait_for_input_message, args=(10, test_client, friend_to_test_input, environment.module_id, result_messages, expected_messages, 0, 1))
        listen_thread.daemon = True
        listen_thread.start()
    else:
        test_input_thread = test_client.wait_for_input_event_async(friend_to_test_input)

    friend_client.send_output_event(friend_to_test_output, sent_message)

    if environment.language == "ppdirect":
        listen_thread.join(10)

        received_message = result_messages[0]
        if not received_message:
            log_message("Message not received")
            assert False
    else:
        received_message = test_input_thread.get(receive_timeout)
        assert received_message == sent_message

    log_message("Disconnecting clients")
    friend_client.disconnect()
    test_client.disconnect()


@pytest.mark.testgroup_edgehub_module_client
@pytest.mark.callsSendOutputEvent
@pytest.mark.receivesInputMessages
def test_module_test_to_friend_and_back():

    test_client = connections.connect_test_module_client()
    test_client.enable_input_messages()
    friend_client = connections.connect_friend_module_client()
    friend_client.enable_input_messages()

    result_messages = [None] * 1
    expected_messages = [None] * 1

    friend_to_test_sent_message = test_utilities.max_random_string()
    expected_messages[0] = friend_to_test_sent_message

    # For direct SDK test client works differently
    if environment.language == "ppdirect":
        listen_thread = threading.Thread(target=wait_for_input_message, args=(
        10, test_client, friend_to_test_input, environment.module_id, result_messages, expected_messages, 0, 1))
        listen_thread.daemon = True
        listen_thread.start()
    else:
        test_input_thread = test_client.wait_for_input_event_async(friend_to_test_input)

    friend_input_thread = friend_client.wait_for_input_event_async(test_to_friend_input)

    test_to_friend_sent_message = test_utilities.max_random_string()
    test_client.send_output_event(test_to_friend_output, test_to_friend_sent_message)

    midpoint_message = friend_input_thread.get(receive_timeout)
    assert midpoint_message == test_to_friend_sent_message

    friend_client.send_output_event(friend_to_test_output, friend_to_test_sent_message)

    if environment.language == "ppdirect":
        listen_thread.join(10)

        received_message = result_messages[0]
        if not received_message:
            log_message("Message not received")
            assert False
    else:
        received_message = test_input_thread.get(receive_timeout)
        assert received_message == friend_to_test_sent_message

    friend_client.disconnect()
    test_client.disconnect()


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
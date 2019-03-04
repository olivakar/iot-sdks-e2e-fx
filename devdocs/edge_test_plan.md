# IoT Edge Test Plan using the Horton Test Framework

This document is an outline of the specific test scenarios we are covering with the IoT Edge tests.

## Related documents

* For a big-picture of the Horton test framework, look [here](.\framework_top_level_picture.md)
* Some definitions useful in understanding the Horton framework are outlined [here](.\framework_definitions.md)
* Examples and visualizations for understanding the definitions are provided [here](.\framework_definitions_visualized.md)

## Definitions

In addition to the definitions used by the Horton framework, the following definitions are useful in describing the Edge E2E tests.
* __test module__ - This is the Edge Module, living inside a docker container, which contains the code that we are testing.
* __friend module__ - This is a secondary Edge module which is used to help validate the test module.  The friend module is used:
    * as a destination for output events that the test module sends
    * as a source for input messages that the test module receives
    * as a receiver for method calls that the test module invokes
    * as an invoker for method calls that the test module receives
* __leaf device__ - This is a limited Azure IoT Device client which is also used to help validate the test module.  The leaf device is used:
    * as a receiver for method calls that the test module invokes

The following names are also known, but they are part of a implementation details that are being phased out.
* __nodeMod__, __cMod__, __csharpMod__, __javaMod__, __pythonMod__, and __pythonPreviewMod__ - these are the names of docker containers that are used as test modules for different langauges.
* __friendMod__ - this is the name of the docker container which is responsible for acting as:
    * The friend module as defined above.
    * The leaf device as defined above.
    * a default implementation of the Service and Registry APIs, in case the module under test does not have an implementation to use for testing.

The fact that friendMod is an Edge module, and also a leaf device and an implementation of other APIs is confusing and should not be dwelt on as these pieces of functionality are eventually moving into their own containers

## Test Environments

Edge Tests are currently being run only under AMD64 Linux (16.04) with the following Docker containers.  Base container choices are somewhat arbitrary.

| SDK | Docker Base Image Name | OS | Language Variant |
| -- | -- | -- | -- |
| C | ubuntu:18.04 | Ubuntu 18.04 | GCC |
| CSharp | microsoft/dotnet:2.2-sdk | Debian Stretch (v9) | .net core 2.2 |
| Java | maven:3.3-jdk-8 | Debian Jesie (v8) | JDK-8 |
| Node | node:6-slim | Debian Stretch (v9)| Node 6.17 |
| Python | ubuntu:18.04 | Ubuntu 18.04 | GCC + Python 3.6 |
| Python-preview |  python:3.6 | Debian Stretch (v9) | Python 3.6.8 |

## Test Suites (or "the matrix of suites")

Tests for the Module Client SDK are run using both EdgeHub and IoTHub as destinations with 4 different transports (AMQP, AMQP-WS, MQTT, MQTT-WS).  This leads us to 8 different suites:
* edgehub_module_amqp
* edgehub_module_amqp_ws
* edgehub_module_mqtt
* edgehub_module_mqtt_ws
* iothub_module_amqp
* iothub_module_amqp_ws
* iothub_module_mqtt
* iothub_module_mqtt_ws

All SDKs run all suites, with two exceptions:
1. C and Python don't run edgehub_module_amqp and edgehub_module_amqpws
2. PythonPreview only runs edgehub_module_mqtt and iothub_module_amqtt

## Test Cases


## Current Exclusions

## Current Pass Rates


cmd
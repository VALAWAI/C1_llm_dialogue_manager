# VALAWAI SR C1 LLM Dialogue Manager

## Description

This C1 component implements a dialogue manager for the Social Robots VALAWAI applications.

A dialogue manager is the core component of conversational systems.
It facilitates coherent and meaningful interactions between the dialogue participants.
The main responsibility of a dialogue manager is selecting the most appropriate response to an input, in order to maintain the flow of the conversation.
To achieve this objective there are many techniques such as rule-based systems, state machines, and reinforcement learning.
This component uses a large language model fine-tuned for this purpose.

In addition, dialogue managers can use various information sources to decide which is the most appropriate response, such as the dialogue history, the user profile, and the context of the conversation.
What sets this component apart from other dialogue managers is that it can accept additional input, called _reflections_, to steer the conversation.
These reflections are used together with the current conversation history and the last input to select the most appropriate response.

The component can be customised with the identifier for the character impersonated by the dialogue manager.

The component runs in a _Docker_ container, and communicates with a _RabbitMQ_ message broker.
As a large language model it supports _OpenAi_ chat models; in the future, support will be added for the _HuggingFace_ models.

## Data Flow

This component uses a single data flow channel (or _topic_ or _routing key_), `valawai.c0.text-interface`, to communicate with the message broker using the `amq.topic` exchange, which broadcasts the messages to all the listeners bound to it with the same routing key.

This channel is intended for dialogue messages containing text.
Subscribing to this channel allows to receive the dialogue messages, and publishing to this channel allows to send them.

The messages exchanged are _JSON_ objects with the following structure:

```json
{
  "version": "0.0.1", // The version of the format.
  "speaker": "AI", // Identifier of the author of the message.
  "text": "Hello, World!", // The text of the message.
  "timestamp": "2019-08-24T14:15:22Z" // The timestamp of the message.
}
```

## Control Flow

This component uses a single control flow channel, `valawai.c2.observations.reflections`, to communicate with the message broker using the `amq.topic` exchange, which broadcasts the messages to all the listeners bound to it with the same routing key.

This channel is intended for observations messages, containing a short text used to control other components.
Specifically, this channel transports reflections on the dialogue and actions of the agent.
Sending messages to this channel allows to influence the dialogue manager.

The messages exchanged are _JSON_ objects with the following structure:

```json
{
  "version": "0.0.1", // The version of the format.
  "text": "Hello, World!", // The text of the message.
  "timestamp": "2019-08-24T14:15:22Z" // The timestamp of the message.
}
```

## Usage

This component receives dialogue messages from the message broker, and sends dialogue messages to the message broker.
Additionally, it receives observations messages from the message broker, and uses them to influence the dialogue manager.
The implementation uses a text prompt to generate the responses from the large language model.

The component is configurable with the following environment variables, with the default value indicated in parentheses:

- RMQ_HOST (`host.docker.internal`) The hostname of the message broker.
- EXCHANGE (`amq.topic`) The exchange to use for dialogue messages.
- TEXT_INTERFACE_KEY (`valawai.c0.text-interface`) The channel to use for dialogue messages.
- REFLECTIONS_INTERFACE_KEY (`valawai.c2.observations.reflections`) The channel to use for observations messages.
- SPEAKER (_AI_) The identifier for the participant in the dialogue.
- MODEL_NAME (`gpt-3.5-turbo`) The name of the model to use.
- PROMPT (None) The prompt to use for the response generation, if not provided a default prompt is used.
- OPENAI_API_KEY (None) The API key for the OpenAi services.

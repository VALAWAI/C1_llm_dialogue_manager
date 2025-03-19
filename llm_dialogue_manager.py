from pathlib import Path

from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import load_prompt
from langchain.schema import ChatMessage
from valawai_sr import Channel, ObservationMessage, TextMessage, env

env.add("speaker", "AI")
"""The identifier for the participant in the dialogue."""

env.add("model_name", "gpt-3.5-turbo")
"""The name of the OpenAI chat model to use for the dialogue."""

env.add("prompt", None)
"""The prompt to use for the response generation, if not provided a default prompt is used."""


class ThoughtMessage(ChatMessage):
    speaker = "Thought"


class InnerMonologue(ConversationSummaryBufferMemory):
    def add_thought(self, thought: str) -> None:
        """Add a thought to the buffer."""
        thought_message = ThoughtMessage(content=thought)
        self.chat_memory.add_message(thought_message)


def main():
    llm = ChatOpenAI(
        temperature=0.9,
        model_name=env.model_name,
    )

    memory = InnerMonologue(
        llm=llm,
        max_token_limit=650,
        ai_prefix=env.speaker,
    )

    if env.prompt is None:
        prompt = load_prompt(Path(__file__).with_name("./prompt.yaml"))
    else:
        prompt = PromptTemplate.from_template(env.prompt)
    prompt = prompt.partial(ai_prefix=env.speaker)
    prompt = prompt.partial(human_prefix="HUMAN")  # FIXME: Human prefix is hardcoded.
    # Human prefix requires multiple inputs, which are not supported by the memory component.
    # Implementing requires too much effort and ConversationChain will probably not be used.

    conv_chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True,
    )

    def new_message(ch, method, properties, body):
        message: TextMessage = TextMessage.from_json(body)
        if message.speaker != env.speaker:
            answer = conv_chain.run(input=message.text)
            print(f"{env.speaker}: {answer}")
            message = TextMessage(speaker=env.speaker, text=answer)
            channel.publish(env.text_interface_key, message)

    def new_reflect(ch, method, properties, body):
        message: ObservationMessage = ObservationMessage.from_json(body)
        memory.add_thought(message.text)
        print("Thought:", message.text)

    channel = Channel()
    channel.configure_consume(env.text_interface_key, new_message)
    channel.configure_consume(env.reflect_interface_key, new_reflect)
    channel.start_consuming()


if __name__ == "__main__":
    main()

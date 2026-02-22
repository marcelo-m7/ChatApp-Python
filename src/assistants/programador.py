from __future__ import annotations

from langchain.prompts import ChatPromptTemplate
from openai import OpenAI

from chatapp.config.assistant import AssistantModelConfig, assistant_config
from chatapp.infrastructure.openai.openai_client import create_openai_client


class Programador:
    def __init__(self, config: AssistantModelConfig | None = None, client: OpenAI | None = None):
        self.config = config or assistant_config
        self.client = client or create_openai_client()
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_prompts}"),
                ("system", "Histórico de conversação:\n{conversation_history}"),
                ("human", "{input}"),
            ]
        )

    def get_response(self, input: str, conversation_history) -> str:
        try:
            prompt_messages = self.prompt_template.format_messages(
                system_prompts="\n".join(self.config.system_prompts),
                conversation_history=str(conversation_history),
                input=input,
            )
            messages = [{"role": message.type, "content": message.content} for message in prompt_messages]

            completion = self.client.chat.completions.create(
                model=self.config.model,
                temperature=self.config.temperature,
                messages=messages,
            )
            return completion.choices[0].message.content
        except Exception:
            return "I'm not feeling ok... Would you mind if we talk another time?"

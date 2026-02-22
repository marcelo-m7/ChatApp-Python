from dotenv import load_dotenv
from openai import OpenAI

from chatapp.config.assistant import AssistantModelConfig, assistant_config

load_dotenv(".env")


class Programador:
    def __init__(self, config: AssistantModelConfig | None = None):
        self.config = config or assistant_config
        self.client = OpenAI()

    def get_response(self, input: str, conversation_history) -> str:
        try:
            messages = [
                {"role": "system", "content": prompt}
                for prompt in self.config.system_prompts
            ]
            messages.append(
                {
                    "role": "system",
                    "content": f"Histórico de conversação:\n {conversation_history}",
                }
            )
            messages.append({"role": "user", "content": input})

            completion = self.client.chat.completions.create(
                model=self.config.model,
                temperature=self.config.temperature,
                messages=messages,
            )
            return completion.choices[0].message.content
        except Exception:
            return "I'm not feeling ok... Would you mind if we talk another time?"

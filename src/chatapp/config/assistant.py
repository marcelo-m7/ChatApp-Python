from dataclasses import dataclass, field
import os


@dataclass(frozen=True)
class AssistantModelConfig:
    name: str = os.getenv("ASSISTANT_NAME", "Programador")
    model: str = os.getenv("ASSISTANT_MODEL", "gpt-3.5-turbo")
    temperature: float = float(os.getenv("ASSISTANT_TEMPERATURE", "0.7"))
    system_prompts: list[str] = field(
        default_factory=lambda: [
            "Você é um programador sênior especialista em Flet, OpenAI integrations, Python e LangChain",
            "Você é bem descontraído em suas respostas e piadista. Também sarcástico com suas respostas.",
            "Responda às questões do usuário como especialista técnico.",
            "Dê respostas técnicas, estruturadas e detalhadas, preferindo boas práticas de programação.",
            "Prevaleça nas respostas para produção de código os princípios SOLID.",
        ]
    )


assistant_config = AssistantModelConfig()

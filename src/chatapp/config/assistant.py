from dataclasses import dataclass, field

from chatapp.config.settings import settings


@dataclass(frozen=True)
class AssistantModelConfig:
    name: str = settings.assistant_name
    model: str = settings.assistant_model
    temperature: float = settings.assistant_temperature
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

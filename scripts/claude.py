import os
from pathlib import Path
from dotenv import load_dotenv
import anthropic
from dataclasses import dataclass

PROMPTS_DIR = Path("prompts")
DEFAULT_MODEL = "claude-3-opus-20240229"
DEFAULT_MAX_TOKENS = 4000
SYSTEM_FN = "system_prompt.txt"
USER_FN = "user_prompt.txt"
RESPONSE_FN = "response.txt"


@dataclass
class StoredPrompt:
    path: Path
    system: str
    user: list[dict[str, str]] 


def get_client() -> anthropic.Client:
    api_key = os.getenv("CLAUDE_API_KEY")
    client = anthropic.Client(api_key=api_key)
    return client


def get_response(
    client: anthropic.Client,
    message: StoredPrompt,
    model: str = DEFAULT_MODEL,
    max_tokens=DEFAULT_MAX_TOKENS,
) -> str:
    response = client.messages.create(
        model=model, system=message.system, messages=message.user, max_tokens=max_tokens
    )
    return response


def get_messages(prompts_dir: Path = PROMPTS_DIR) -> list[StoredPrompt]:
    messages = []

    for path in prompts_dir.iterdir():

        if path.is_dir():
            system = (path/SYSTEM_FN).read_text()
            user_content = (path/USER_FN).read_text()
            user = [{"role": "user", "content": user_content}]
            messages.append(StoredPrompt(path=path, system=system, user=user))
    return messages


def main() -> None:
    load_dotenv()
    print(os.getenv("CLAUDE_API_KEY"))
    client = get_client()
    messages = get_messages()
    for message in messages:
        response = get_response(client, message)
        response_fn = message.path/RESPONSE_FN
        response_fn.write_text(response.content[0].text)


if __name__ == "__main__":
    main()

import os
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Client
from anthropic.types import Message, MessageParam
from dataclasses import dataclass
from warnings import warn


PROMPTS_ROOT = Path("prompts")
DEFAULT_MODEL = "claude-3-opus-20240229"
DEFAULT_MAX_TOKENS = 4000
SYSTEM_FN = "system_prompt.txt"
USER_FN = "user_prompt.txt"
RESPONSE_FN = "response.txt"
HASH_FN = "hash.sha256"


@dataclass
class StoredPrompt:
    path: Path
    system: str
    user: list[MessageParam]

    def sha256(self) -> str:
        return hashlib.sha256(
            (self.system + str(self.user)).encode("utf-8")
        ).hexdigest()


def get_client() -> Client:
    api_key = os.getenv("CLAUDE_API_KEY")
    client = Client(api_key=api_key)
    return client


def get_response(
    client: Client,
    message: StoredPrompt,
    model: str = DEFAULT_MODEL,
    max_tokens=DEFAULT_MAX_TOKENS,
) -> Message:
    response = client.messages.create(
        model=model, system=message.system, messages=message.user, max_tokens=max_tokens
    )
    return response


def get_prompts(prompts_root: Path = PROMPTS_ROOT) -> list[StoredPrompt]:
    messages = []

    # iterate through subdirs of the prompts directory
    for path in prompts_root.iterdir():
        if path.is_dir():
            # read the system and user prompts from the files
            system = (path / SYSTEM_FN).read_text()
            user_content = (path / USER_FN).read_text()
            user = [MessageParam(role="user", content=user_content)]
            prompt = StoredPrompt(path=path, system=system, user=user)

            # check if the hash of the prompt is already stored, skip if so
            new_hash = prompt.sha256()
            stored_hash_fn = path / HASH_FN
            if stored_hash_fn.exists():
                stored_hash = stored_hash_fn.read_text()
                if stored_hash == new_hash:
                    warn(f"Skipping prompt {path}, hash already exists")
                    continue
                else:
                    warn(f"Hash mismatch for prompt {path}, overwriting")

            messages.append(prompt)

    return messages


def write_response(response: Message, prompt: StoredPrompt) -> None:
    response_fn = prompt.path / RESPONSE_FN
    response_fn.write_text(response.content[0].text)
    hash_fn = prompt.path / HASH_FN
    hash_fn.write_text(prompt.sha256())


def main() -> None:
    load_dotenv()
    print(os.getenv("CLAUDE_API_KEY"))
    client = get_client()
    prompts = get_prompts()
    for prompt in prompts:
        response = get_response(client, prompt)
        write_response(response, prompt)


if __name__ == "__main__":
    main()

import json
from typing import Callable
from .message import Message

Counter = Callable[[str], int]


def estimate_tokens(text: str) -> int:
    """~4 chars per token. Works for any model, accurate to roughly 10-20%."""
    return (len(text) + 3) // 4


def message_tokens(message: Message, counter: Counter = estimate_tokens,
                   per_message_overhead: int = 4, image_tokens: int = 1_600) -> int:
    """Estimate tokens for a single message."""
    n = per_message_overhead
    for part in message.content or []:
        if part.type == 'text':
            n += counter(part.data.get('text', ''))
        elif part.type == 'image':
            n += image_tokens
        else:
            n += counter(json.dumps(part.data, default=str))
    for call in message.tool_calls or []:
        n += counter(call.name) + counter(json.dumps(call.args or {}, default=str))
    return n


def count_tokens(messages: list[Message], tools: list[dict] | None = None,
                 counter: Counter = estimate_tokens, **kwargs) -> int:
    """Estimate total tokens for a list of messages plus optional tool schemas.

    kwargs are passed through to message_tokens (per_message_overhead, image_tokens).
    """
    total = sum(message_tokens(m, counter, **kwargs) for m in messages)
    if tools:
        total += counter(json.dumps(tools, default=str))
    return total

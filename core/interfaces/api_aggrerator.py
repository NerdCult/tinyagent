from typing import Protocol, Iterator
from ...messages import TARecord, AgentMessage


class ApiAggregator(Protocol):
    def process_context(self, context: list[TARecord]) -> Iterator[AgentMessage]: ...
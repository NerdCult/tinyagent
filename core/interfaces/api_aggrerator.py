#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

from typing import Protocol, Iterator
from ...messages import TARecord, AgentMessage


class ApiAggregator(Protocol):
    '''
    recieves the context from the AgentRuntime, passes to the API Client, handles the ApiEvents; 
    passes deltas through as AgentMessages for responsive user experince
    aggregates the deltas to create TARecords and passes them through for the AgentRuntime to process
    '''
    def process_context(self, context: list[TARecord]) -> Iterator[AgentMessage]: ...
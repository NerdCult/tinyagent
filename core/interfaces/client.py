from typing import Protocol, Iterator, runtime_checkable
from ...messages.api_event import ApiEvent
from ...messages.ta_record import TARecord

@runtime_checkable 
class Client(Protocol):
    ''' provides interaction with the api for chat completions. 
        Must accept a list of Tiny Agent TaRecords and convert to the expected api format.
        Must return an Iterator of the Tiny Agent ApiEvent'''
    def get_stream(self, messages: list[TARecord], tools: list[dict] | None = None) -> Iterator[ApiEvent]: ...
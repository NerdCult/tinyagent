#for future development
    # def part_to_anthropic(self, part: Part) -> dict:
    #     """Adapt this Part into an Anthropic-wire part dict."""
    #     if part.type == "text":
    #         return {"type": "text", "text": part.data.get("text", "")}
    #     elif part.type == "image":
    #         return {"type": "image", "source": {
    #             "type": "base64", "media_type": part.data.get("media_type"),
    #             "data": part.data.get("data", "")
    #         }}
    #     return {"type": part.type, **part.data}

    # def message_to_anthropic(self, message: Message) -> dict:
    #      if message.role == "assistant":
    #          result = {"role": "assistant"}
    #          result["content"] = [self.part_to_anthropic(p) for p in message.content]
    #          if message.tool_calls:
    #              result["tool_calls"] = [tc.to_anthropic() for tc in message.tool_calls]
    #          return result
    
    #      if message.role == "tool":
    #          return {
    #              "role": "user",
    #              "content": [{"type": "tool_result",
    #                           "tool_use_id": message.tool_call_id,
    #                           "content": message.content[0].data.get("text", "")}]
    #          }
    
    #      return {"role": message.role, "content": [self.part_to_anthropic(p) for p in message.content]}
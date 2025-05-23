from pydantic import BaseModel
from typing import Optional, Literal


# pydanic models for request & response validation

# structure of requests
class GenerationRequest(BaseModel):
    model_name: Literal["llama-1b", "llama-3b"]
    prompt: str
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.0


    class Config: 
        protected_namespaces = () # tell system there are no protected name spaces bc it keeps popping up as a warning in the terminal

#structure of responses
class GenerationResponse(BaseModel):
    text: str
    model_used: str


    class Config:
        protected_namespaces = ()

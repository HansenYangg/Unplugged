from fastapi import FastAPI, HTTPException
from models import GenerationRequest, GenerationResponse
from llms import LLMManager
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from conversation import ConversationHandler
from fastapi.responses import StreamingResponse
from collections.abc import AsyncGenerator
from fastapi.responses import StreamingResponse
from asyncio import Lock as AsyncLock


app = FastAPI(title="Offline LLM Backend") # handle cross origin requests

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with frontend URL (?)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_manager = LLMManager() # handles the LLM interactions (from llm.py)
conversation_manager = ConversationHandler() # handles conversation history


@app.get("/health")
async def health_check():
    return {"status": "ok"} # checks that server is running fine


@app.post("/generate", response_model=GenerationResponse) # create endpoint that accepts requests with parameters

async def generate_text(request: GenerationRequest): # responsible for actually generating the response based on the request content
    try:
       
        if not conversation_manager.history_exists():
            p = request.prompt
        else:
            conversation_manager.get_conversation_history()
            p = f"Based on this conversation: {conversation_manager.get_conversation_history()},\nprovide a concise and relevant assistant response to this user prompt: {request.prompt}."

        generated_text = llm_manager.generate(model_name=request.model_name, 
            prompt=p,
            
            
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

       
        conversation_manager.add_message(request.prompt, "User")
        conversation_manager.add_message(generated_text, "Assistant")
        
        
        return GenerationResponse(
            text=generated_text,
            model_used=request.model_name
        )
    except Exception as e: 

        raise HTTPException(status_code=500, detail=str(e))

from fastapi.responses import StreamingResponse





@app.post("/generate-stream")
async def generate_stream(request: GenerationRequest):
    if not conversation_manager.history_exists():
        p = request.prompt
    else:
        if request.model_name == "llama-1b":
            
            p = f"You are an assistant interacting with a user. Here are you previously exchanged messages with the user:\n{conversation_manager.get_conversation_history()}.\nCarefully construct a very concise and relevant response that completely addresses this user's new prompt, which is: {request.prompt}.\nExplicitly state only your response to this user with five or more words unless told otherwise.\nDo not include old conversation messages in your response and do not try to generate new conversation.\nNow, you MUST generate ONLY a detailed response to the user.\nHere is the response:" #prev MUST generate ONLY a detailed response to the
           
            
        else:
            p = f"Based on this conversation: {conversation_manager.get_conversation_history()},\nprovide a very concise and relevant response ONLY to this user prompt: {request.prompt}.\nDO NOT mention any old conversation.\nDO NOT generate extra conversation.\nNow, give ONLY your reply."
    async def generate():
        try:
            full_response = ""
            # first_line = None
            for text_chunk in llm_manager.generate_stream(
                model_name=request.model_name,
                prompt=p,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            ):
                full_response += text_chunk
                # if not first_line and '\n' in full_response:
                #     first_line = full_response.split('\n')[0]
                yield text_chunk
            
            if full_response != "":
                # print(first_line)
                # print("Here" in first_line)
                # print('test')
                # if first_line is not None and "Here" in first_line and "is" in first_line:
                #     full_response = full_response.split('\n', 1)[1].strip()
                conversation_manager.add_message(request.prompt, "User")
                conversation_manager.add_message(full_response, "Assistant")
                print(conversation_manager.get_conversation_history())
            
        except Exception as e:
            print(f"Error in generate_stream: {str(e)}")

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )


# start local server using port 8000 
if __name__ == "__main__":
    print("Starting server..")
    conversation_manager.clear_history()
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Failed to start server: {str(e)}")

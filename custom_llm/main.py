from fastapi import FastAPI
from ctransformers import AutoConfig
from ctransformers import AutoModelForCausalLM
from pydantic import BaseModel

from util import ocr


# Pydantic model to represent the request body the Cat sends
class RequestBody(BaseModel):
    text: str
    auth_key: str | None = None
    option: dict | None = None


# FastAPI app
app = FastAPI()

config = AutoConfig.from_pretrained("./model/llama-2-7b-chat.ggmlv3.q2_K.bin")
config.config.max_new_tokens = 2048
config.config.context_length = 4096

# Llama2 model instantiated with CTransformers
llm = AutoModelForCausalLM.from_pretrained('./model/llama-2-7b-chat.ggmlv3.q2_K.bin', model_type='llama', gpu_layers=0, config=config)


@app.on_event("startup")
async def startup():
    print("FastAPI is starting up!")
    print("Using OCR approach we have to extract file content into other file/s into ../cat/static/ocr/ folder.")
    print("Then with the import ocr docs plugin cheshire-cat will put this content inside rabbit hole.")
    ocr.ocr_procedure()


# GET endpoint method
@app.get("/custom-llm")
async def test_get():
    return {"message": "Here we are folks!"}


# POST endpoint method that uses Llama2 to generate a response using
# the user's text received
@app.post("/custom-llm/")
async def root(request_body: RequestBody):
    answer = llm.__call__(prompt = request_body.text, max_new_tokens = 512, repetition_penalty = 1.3)
    return {"text": answer}

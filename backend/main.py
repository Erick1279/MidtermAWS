from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import uuid
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('UrlShortener')

class URLRequest(BaseModel):
    original_url: str

@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_code = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    
    table.put_item(
        Item={
            'short_code': short_code,
            'original_url': request.original_url,
            'created_at': created_at
        }
    )
    
    return {
        "short_code": short_code,
        "original_url": request.original_url,
        "short_url": f"http://<IP_EC2>:8000/{short_code}"
    }

@app.get("/{short_code}")
def redirect_url(short_code: str):
    response = table.get_item(Key={'short_code': short_code})
    if 'Item' not in response:
        raise HTTPException(status_code=404, detail="Not Found")
    return RedirectResponse(url=response['Item']['original_url'], status_code=307)

@app.get("/urls/{short_code}")
def get_url_info(short_code: str):
    response = table.get_item(Key={'short_code': short_code})
    if 'Item' not in response:
        raise HTTPException(status_code=404, detail="Not Found")
    return response['Item']
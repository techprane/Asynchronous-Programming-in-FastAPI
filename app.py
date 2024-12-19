from fastapi import FastAPI, BackgroundTasks
import httpx
import aiofiles
import pytest
from fastapi.testclient import TestClient

app = FastAPI()

# API Endpoints
@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/external-api")
async def call_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/posts/1")
    return response.json()

@app.get("/read-file")
async def read_file():
    async with aiofiles.open("example.txt", mode="r") as file:
        content = await file.read()
    return {"content": content}

def send_email(email: str, message: str):
    print(f"Sending email to {email} with message: {message}")

@app.post("/send-email/")
async def schedule_email(background_tasks: BackgroundTasks, email: str):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Email scheduled"}

# Testing Code
client = TestClient(app)

def test_read_item():
    response = client.get("/item/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}

def test_read_file():
    # Create an example file for testing
    with open("example.txt", "w") as file:
        file.write("This is a test file content")

    response = client.get("/read-file")
    assert response.status_code == 200
    assert response.json() == {"content": "This is a test file content"}

def test_schedule_email():
    response = client.post("/send-email/?email=fogigav197@rabitex.com")
    assert response.status_code == 200
    assert response.json() == {"message": "Email scheduled"}

@pytest.mark.asyncio
async def test_call_external_api():
    async with httpx.AsyncClient() as async_client:
        response = await async_client.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200
    assert "id" in response.json()

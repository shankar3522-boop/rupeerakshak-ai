# Backend

## Directory Structure
- src/
  - main.py
  - app/
    - __init__.py
    - api/
    - models/
    - services/
- requirements.txt

## FastAPI Initialization

```python
from fastapi import FastAPI
  
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

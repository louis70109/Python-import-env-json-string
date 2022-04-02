import tempfile
import os

if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv

    load_dotenv()

import uvicorn
import json
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    print('=' * 20)
    print(os.environ['SOME_KEY'])
    with open(os.environ['SOME_KEY']) as f:
        lines = f.read()
        print(lines)
        print(type(lines))
    return {"SOME_KEY": json.loads(lines)}


if __name__ == "__main__":
    temp = tempfile.NamedTemporaryFile(suffix='.json')
    try:
        SOME_KEY = os.environ.get('SOME_KEY', '{}')
        temp.write(SOME_KEY.encode())
        temp.seek(0)
        print(temp.read())
        print(temp.name)
        os.environ['SOME_KEY_PATH'] = temp.name
        uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    finally:
        temp.close()

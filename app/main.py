from fastapi import FastAPI
import numpy as np

zeros = np.zeros((4, 4))
print(zeros)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
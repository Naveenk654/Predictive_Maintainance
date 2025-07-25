from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Any,Annotated
from pydantic import BaseModel, Field
import pandas as pd
import pickle
app=FastAPI()
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)    
class UserInput(BaseModel):
    Type: str=Field(...)
    Air_temperature: float = Field(..., alias="Air temperature [K]")
    Process_temperature: float = Field(..., alias="Process temperature [K]")
    Rotational_speed: float = Field(..., alias="Rotational speed [rpm]")
    Torque: float = Field(..., alias="Torque [Nm]")
    Tool_wear: float = Field(..., alias="Tool wear [min]")

    class Config:
        populate_by_name = True #Because here we can see in our data the names are different so we have to use it

@app.post('/predict')
def pred_failure_type(input_data: UserInput):

    input_df = pd.DataFrame([input_data.dict(by_alias=True)])

    #
    prediction = int(model.predict(input_df)[0])
 
    
    failure_label = str(label_encoder.inverse_transform([prediction])[0])
   
    return {"predicted_failure_type": failure_label}


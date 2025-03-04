from fastapi import FastAPI, File, UploadFile
from inference_sdk import InferenceHTTPClient
from PIL import Image
import io

app = FastAPI()

# Initialize Roboflow API Client
CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="TRxsXEBYL63UjS4LbQMk"
)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read image
    image = Image.open(io.BytesIO(await file.read()))
    
    # Save temp image
    temp_path = "temp.jpg"
    image.save(temp_path, format="JPEG")

    # Send image to Roboflow API
    result = CLIENT.infer(temp_path, model_id="food-spoilage-status-axom2/7")
    
    predictions = result.get("predictions", [])
    response_data = []

    for pred in predictions:
        food_class = pred.get("class", "Unknown")
        confidence = pred.get("confidence", 0) * 100  # Convert to percentage
        response_data.append({"food": food_class, "confidence": confidence})
    
    return {"predictions": response_data}

# Run the API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

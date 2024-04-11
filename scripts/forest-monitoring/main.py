"""
Script to run the forest monitoring pipeline
"""

from spai.analytics.forest_monitoring import forest_monitoring
from spai.storage import Storage
from tqdm import tqdm
from spai.config import SPAIVars

storage = Storage()["data"]
vars = SPAIVars()


if __name__ == "__main__":
    collection = "sentinel-2-l2a"
    images = storage.list(f"{collection}*.tif")
    aoi = vars["AOI"]
    for image in tqdm(images, desc="Processing images..."):
        forest_monitoring(image, aoi, storage)

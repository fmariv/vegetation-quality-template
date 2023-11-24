from os.path import join

from tqdm import tqdm

from spai.storage import Storage
from spai.pulses import forest_monitoring
from spai.project import ProjectConfig

storage = Storage("data")

project = ProjectConfig()


if __name__ == '__main__':
    sensor = "S2L2A"  # or 'S2L1C'
    images = storage.list(f"{sensor}*.tif")
    aoi = project.aoi
    for image in tqdm(images, desc="Processing images..."):
        forest_monitoring(
            image,
            aoi,
            storage
        )

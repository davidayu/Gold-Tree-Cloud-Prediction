# Gold-Tree-Cloud-Prediction
Gold Tree Solar Farm is an 18.5-acre solar farm with approximately 16,000 solar panels, and a capacity of 4.5 MW DC. One of the challenges with integrating solar energy into the energy grid is that the peak electrical demand doesn’t coincide with peak power generation from solar fields. Solar energy is also considered an unreliable energy source because production vary significantly depending on the weather conditions. Utilities are often required to balance solar generation to meet consumer demand, which often includes the costly process of activating/deactivating a fossil fuel facility. Therefore, there is considerable interest in increasing the accuracy and the granularity of solar power generation forecasting. This better forecasting would reduce fluctuations of the electrical grid and facilitate its management. In this project, our goal is to be able to forecast with accuracy cloud coverage over a solar field up to 30 min into the future. The predictions are based on computer vision techniques that analyze total sky images deployed in the field.

cloud_cover.py analyzes a sky camera image and returns the cloud cover % 

download_sky_images.py is used to download sky camera images

generate_dataset_script.py is used to combine our historical weather data with our cloud cover data into a CSV to be used for ML training

# Unsupervised Clustering of Global Climate Zones using HDBSCAN
This project explores whether established Köppen-Geiger 
climate zones can be rediscovered using a purely data-driven, 
unsupervised machine learning approach. 
The primary goal is to apply the HDBSCAN clustering algorithm 
to a raster stack of global climate variables (e.g., temperature, precipitation) 
and evaluate how well the resulting clusters align with the well-known Köppen-Geiger 
classification map.

## Motivation
The classification of global climates into distinct zones is fundamental to understanding 
Earth's ecosystems. While the Köppen-Geiger system is a widely used, rule-based standard, 
this project investigates if these zones can be found organically through machine learning.

There are two main advantages:

- Adaptability to Climate Change: An unsupervised model can be easily re-run with updated 
climate data to monitor how climate zones are shifting over time.

- Flexibility in Research: The framework allows for the inclusion of different variables 
(for example vegetation data like NDVI) to create custom climate classifications tailored to 
specific research questions.

The HDBSCAN algorithm was chosen for its ability to handle complex, non-linear data, identify 
clusters of varying densities and shapes, and its robustness against noise, making it ideal for 
climatological data.

## Getting started
A ready-to-go virtual environment can be set up with pyproject.toml

Requires-python >=3.12

Dependencies:
- geopandas (>=1.1.1,<2.0.0)
- rasterio (>=1.4.3,<2.0.0)
- scikit-learn (>=1.7.2,<2.0.0)
- hdbscan (>=0.8.40,<0.9.0)
- matplotlib (>=3.10.6,<4.0.0)
- seaborn (>=0.13.2,<0.14.0)

## Data
The workflow can be run with the data you find in the data directory.
Use the feature_stack.tif file for run the clustering algorithm.
Your result can be stacked with the koppen_geiger_reclass.tif for evaluation.
An example for a cluster result produced by the presented pipline can be found 
in evaluation_stack.tif. Band 1 holds the reference data from the Köppen-Geiger map,
band 2 are the resulting classes.
If you want to use your own climate variables, you can stack your GeoTIFF files
with the raster_stack.py script.

## Usage
The workflow is divided into multiple steps. Use the scripts to run the clustering pipeline.
1. Prepare a raster stack: Climate variables in the GeoTIFF format can be stacked into one file with 
raster_stack.py
2. Run the Clustering: The main.py script executes the entire clustering pipeline. It calls multiple
classes to prepare the input data, run the clustering and safe the result to a new GeoTIFF file.
The input should be a raster stack with the input features, located in the data directory.
3. Reclassification: The reference data (Köppen-Geiger map) can be reclassified to display only
the five main climate zones. Your resulting clusters also can be classified with raster_reclassification.py.
For this step, a visual evaluation and interpretation of the clusters is important. Noise should be
labeled with 0 and mixed classes (clusters that can not be affiliated with one climate zone) with 6.
4. Raster Alignment: The result file will likely have different cell shape than the reference data.
Align them with raster_alignment.py and stack them into one GeoTIFF file to ensure safe result evaluation. 
5. Evaluate the Results: The method_evaluation.py script compares the generated clusters with a reference map. 
It creates a confusion matrix, evaluation report and the Area Under the Curve value.
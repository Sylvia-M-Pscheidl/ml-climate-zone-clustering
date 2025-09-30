# Technical Documentation
This document provides a technical overview of the scripts and methodology used to perform 
unsupervised clustering of global climate zones. The resulting clusters get compared to
the five main climate zones defined bei Köppen and Geiger.

## Core Dependencies
A ready-to-go virtual environment can be set up with pyproject.toml

Requires-python >=3.12

Dependencies:
- geopandas (>=1.1.1,<2.0.0)
- rasterio (>=1.4.3,<2.0.0)
- scikit-learn (>=1.7.2,<2.0.0)
- hdbscan (>=0.8.40,<0.9.0)
- matplotlib (>=3.10.6,<4.0.0)
- seaborn (>=0.13.2,<0.14.0)

## Workflow Methodology and Scripts
### Preparing the feature file
A set of GeoTIFF files holding worldwide climate data can be stacked into one multi-band GeoTIFF file with
**raster_stack.py**. The script ensures all features are aligned to a common spatial grid by using the metadata from the first input raster as the reference for the output stack.

### Clustering
The actual clustering happens when using **main.py** that calls necessary functions in **classes.py**.

#### Data Preparation
The multi-band raster is read in using *src.read()*. The files nodata value is identified from the metadata.
This value is replaced with np.nan. 

HDBSCAN algorithm expect a 2D array. The raster data (3D) gets reshaped using *data.transpose(1,2,0)*.
After that there are two rows, one holding the pixels and the other one the values (climate variable).

A boolean mask is generated to identify if any row contains one or more np.nan values. If so, the
whole row gets excluded. 

#### HDBSCAN Clustering
Before clustering, the prepared data is scaled using *sklearn.preprocessing.SandardScaler*. Each
feature gets standardizes to have a mean of 0 and standard deviation of 1.

The HDBSCAN model is initialized with the parameters *min_cluster_size* and *min_samples*. 
Those get set by the user in the **main.py** script. Then the *.fit()* method is called 
and the clustering process starts.

The labelling is set to start at 0 instead of -1 with *adjusted_labels = original_labels + 1*.

#### Saving Results
the resulting cluster labels get transformed back into the geospatial format with the before
created **valid_data_mask** the ensures that every cluster label gets into their correct spatial position.
A new single-band GeoTIFF, preserving the original spatial reference with the cluster results is created.

### Raster Reclassification
The results might need to be reclassified to match the values of the reference data. Which clusters
represent which climate zone needs to be visually detected by the user. Noise can be labeled with 0 and
clusters, that don`t match well any climate zone can be labeled with 6 (mixed zones). 1 to 5 correspond
to the five main climate zones of the Köppen-Geiger map.
The script *raster_reclassification.py** reads in the result GeoTIFF file into a numpy array and
exchanges the values with a user defined change-matrix.

### Raster Alignment
The script **raster_alignment.py** aligns the reference and result rasters and stacks them into one
multi-band raster file. This is necacary for evaluation, for which the reference and result rasters
need to share the exact same spatial grid (dimension, resolution and CRS). The script uses *rasterio.warp.reproject* 
with nearest neighbor resampling, which is critical for preserving the discrete values of 
categorical data.

### Evaluation metrics
The script **method_evaluation.py** provides a quantitative assessment of the clustering results against the
Köppen_Geiger reference data.
The input data is a GeoTIFF file with two aligned bands, the result and the reference band.
Band 1 (Köppen-Geiger) contains the ground truth data *(y_true)* and Band 2 the predicted cluster labels
*(y_pred)*. With *sklearn.metrics* the confusion matrix, classification report (precission, recall 
and f1-score) and AUC value are generated.
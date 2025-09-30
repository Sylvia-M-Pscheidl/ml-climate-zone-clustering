import rasterio
import numpy as np
import hdbscan
from sklearn.preprocessing import StandardScaler


class DataPreparation:
    """
    Prepares the input raster stack of climate variables
    """
    def __init__(self, raster_stack_path):
        """
        Initializes the DataPreparation object
        """
        self.raster_stack_path = raster_stack_path
        self.profile = None
        self.original_shape = None

    def prepare_data(self):
        """
        Reads the raster stack, reshapes it into a 2D array, and removes rows with NaN values.
        Returns: - A cleaned 2D numpy array holding all features and their values
                 - A mask of the valid data cells, for excluding not complete pixels
        """
        with rasterio.open(self.raster_stack_path) as src:
            self.profile = src.profile
            self.original_shape = (src.height, src.width)

            nodata_value = src.nodata
            # Read all bands into a 3D numpy array
            data = src.read().astype(np.float32)

            # Replaces missing values with NaN for safer handling
            if nodata_value is not None:
                data[data == nodata_value] = np.nan

            # Multiply all values by 100 to dewarp the feature space
            data = data * 1000

            # Reshape to a 2D array
            reshaped_data = data.transpose(1, 2, 0).reshape(-1, src.count)

        # Create a mask for rows that have one or more NaN values
        valid_data_mask = ~np.any(np.isnan(reshaped_data), axis=1)

        # Clean the data from rows with one or more NaN values
        cleaned_data = reshaped_data[valid_data_mask]

        return cleaned_data, valid_data_mask

class HdbscanRun:
    """
    Execute the HDBSCAN clustering algorithm
    """
    def __init__(self, min_cluster_size=500, min_samples=5):
        """
        Initializes the HdbscanRun object.
        """
        self.clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            core_dist_n_jobs=-1
        )
        self.scaled_data = None

    def run_clustering(self, data):
        """
        Performs HDBSCAN clustering
        Returns: Cluster labels for each data point
        """
        # Scales data for balancing feature importance
        self.scaled_data = StandardScaler().fit_transform(data)
        self.clusterer.fit(self.scaled_data)

        # Moves up label numbers so cluster labels start at 1 instead of 0
        original_labels = self.clusterer.labels_
        adjusted_labels = original_labels + 1
        return adjusted_labels

class SaveResults:
    """
    Saves the clustering results back to a GeoTIFF file
    """
    def __init__(self, profile):
        """
        Initializes the SaveResults object
        """
        self.profile = profile

    def save_to_tif(self, output_path, cluster_labels, valid_data_mask, original_shape):
        """
        Saves the cluster labels as a new GeoTIFF file
        """
        nodata_value = -9999
        output_raster = np.full(original_shape[0] * original_shape[1], nodata_value, dtype=np.int32)

        # Place the cluster labels back into their original positions
        output_raster[valid_data_mask] = cluster_labels

        # Reshape the raster to original shape
        output_raster = output_raster.reshape(original_shape)

        # Update the profile for the output raster
        self.profile.update(
            dtype=rasterio.int32,
            count=1,
            nodata=nodata_value
        )

        with rasterio.open(output_path, 'w', **self.profile) as dst:
            dst.write(output_raster.astype(rasterio.int32), 1)
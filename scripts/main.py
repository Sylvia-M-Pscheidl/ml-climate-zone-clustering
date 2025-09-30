from classes import *


if __name__ == '__main__':
    INPUT_RASTER_STACK = r'../data/feature_stack.tif'
    OUTPUT_CLUSTERED_RASTER = r'../output/cluster_result.tif'

    MIN_CLUSTER_SIZE = 30000
    MIN_SAMPLES = 150

    # Data preparation
    print('Preparing the data')
    data_preparer = DataPreparation(INPUT_RASTER_STACK)
    prepared_data, valid_data_mask = data_preparer.prepare_data()
    print('Data preparation complete')

    # HDBSCAN run
    print('Running HDBSCAN clustering')
    hdbscan_runner = HdbscanRun(min_cluster_size=MIN_CLUSTER_SIZE, min_samples=MIN_SAMPLES)
    cluster_labels = hdbscan_runner.run_clustering(prepared_data)
    num_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
    print(f'HDBSCAN complete. Found {num_clusters} clusters')

    # Save results
    print('Saving the results to a GeoTIFF')
    result_saver = SaveResults(data_preparer.profile)
    result_saver.save_to_tif(
        OUTPUT_CLUSTERED_RASTER,
        cluster_labels,
        valid_data_mask,
        data_preparer.original_shape
    )
    print('Clustering results saved')
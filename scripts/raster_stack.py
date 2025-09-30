import rasterio
import glob


def create_raster_stack(input_files, output_file):
    """
    Stacks multiple single-band raster files into a single multi-band raster.
    """

    # Read the metadata from the first file
    with rasterio.open(input_files[0]) as src0:
        meta = src0.meta

    # Update the metadata to reflect the number of bands in the new stack
    meta.update(count=len(input_files))

    # Read each file and write it to a band in the output stack
    with rasterio.open(output_file, 'w', **meta) as dst:
        for id, layer in enumerate(input_files, start=1):
            with rasterio.open(layer) as src1:
                dst.write_band(id, src1.read(1))


if __name__ == '__main__':
    INPUT_RASTER_DIR = 'your_climate_data_directory/'
    RASTER_FILES = glob.glob(f"{INPUT_RASTER_DIR}*.tif")


    # RASTER_FILES = [
    #     # r'../data/wc2.1_10m_bio_1.tif',
    #     # r'../data/wc2.1_10m_tavg_01.tif',
    #     r'../data/wc2.1_10m_srad_01.tif',
    #     r'../data/wc2.1_10m_tmax_01.tif',
    #     r'../data/wc2.1_10m_vapr_01.tif',
    #     r'../data/wc2.1_10m_tmin_01.tif',
    #     r'../data/wc2.1_10m_prec_01.tif',
    #     # r'../data/wc2.1_10m_bio_7.tif',
    #     # r'../data/wc2.1_10m_tavg_07.tif',
    #     r'../data/wc2.1_10m_srad_07.tif',
    #     r'../data/wc2.1_10m_tmax_07.tif',
    #     r'../data/wc2.1_10m_vapr_07.tif',
    #     r'../data/wc2.1_10m_tmin_07.tif',
    #     r'../data/wc2.1_10m_prec_07.tif',
    # ]

    RASTER_FILES = [
        r'../data/koppen_geiger_reclass.tif',
        r'../data/cluster32_reclass.tif'
        ]


    OUTPUT_STACK_FILE = r'../data/evaluation_stack.tif'
    create_raster_stack(RASTER_FILES, OUTPUT_STACK_FILE)
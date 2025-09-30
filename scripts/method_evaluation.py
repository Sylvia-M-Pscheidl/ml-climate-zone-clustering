import rasterio
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from sklearn.preprocessing import label_binarize
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def analyze_stacked_raster(stacked_raster_file):
    """
    Reads a 2 band raster file, compares the bands for the values
    and generates a confusion matrix, classification metrics, and AUC score
    """

    # Values of the classes to include in the analysis. Noise and mixed zones get ignored
    LABELS_TO_KEEP = [1, 2, 3, 4, 5]
    # Climate zone names for plots
    CLASS_NAMES = ['Tropical', 'Dry', 'Temperate', 'Continental', 'Polar']

    with rasterio.open(stacked_raster_file) as src:
        band1_actual = src.read(1)
        band2_predicted = src.read(2)
        nodata_value = src.nodata

        # Create mask to select only valid pixels for the classes
        mask_nodata = (band1_actual != nodata_value) & (band2_predicted != nodata_value)
        mask_labels_actual = np.isin(band1_actual, LABELS_TO_KEEP)
        mask_labels_predicted = np.isin(band2_predicted, LABELS_TO_KEEP)

        # Final mask includes all conditions
        final_mask = mask_nodata & mask_labels_actual & mask_labels_predicted

        y_true = band1_actual[final_mask]
        y_pred = band2_predicted[final_mask]

        # Create confusion matrix
        cm = confusion_matrix(y_true, y_pred, labels=LABELS_TO_KEEP)
        cm_df = pd.DataFrame(cm, index=CLASS_NAMES, columns=CLASS_NAMES)
        cm_df.index.name = 'Actual (Köppen-Geiger)'
        cm_df.columns.name = 'Predicted (HDBSCAN)'
        print(cm_df)

        plt.figure(figsize=(12, 9))
        sns.heatmap(cm_df, annot=True, fmt='d', cmap='viridis',
                    xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
        plt.title('Confusion Matrix: Köppen-Geiger vs. HDBSCAN Clusters')
        plt.show()

        # classification metrics
        print("Classification Report (Precision, Recall, F1-Score)")
        report = classification_report(y_true, y_pred, labels=LABELS_TO_KEEP,
                                       target_names=CLASS_NAMES, zero_division=0)
        print(report)

        # Area Under the Curve
        print("Area Under the Curve (AUC)")

        y_true_binarized = label_binarize(y_true, classes=LABELS_TO_KEEP)
        y_pred_binarized = label_binarize(y_pred, classes=LABELS_TO_KEEP)

        # Calculate AUC
        auc_score = roc_auc_score(y_true_binarized, y_pred_binarized, multi_class='ovr', average='macro')
        print(f"Macro-Averaged AUC (One-vs-Rest): {auc_score:.4f}")


if __name__ == '__main__':
    STACKED_RASTER_FILE = r'../data/evaluation_stack.tif'
    analyze_stacked_raster(STACKED_RASTER_FILE)
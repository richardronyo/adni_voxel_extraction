import nibabel as nib
import numpy as np
import pandas as pd
import os
"""
This function takes the filename of the brain scan you wish to be analyzed, and returns a CSV file that contains all of the FA scores for the 7 masks found in the directory

Parameters: img_name -> filename of the .nii.gz file. Assumming that the photo has been preprocessed according to TBSS protocols and is ready to be masked.

Returns: None

Results: 7 files containing the FA scores for each voxel in the masked region. voxel_<region>.csv 
"""
def extract(img_name):
    masks = ["cingulum_cingulate_gyrus_L.nii.gz", "cingulum_cingulate_gyrus_R.nii.gz", "cingulum_hippocampus_L.nii.gz", "cingulum_hippocampus_R.nii.gz", "corpus_callosum_body.nii.gz", "corpus_callosum_genu.nii.gz", "corpus_callosum_splenium.nii.gz"]

    fa_img = nib.load(img_name)

    for mask in masks:
        roi_mask = nib.load(mask)

        fa_data = fa_img.get_fdata()
        
        roi_data = roi_mask.get_fdata()

        roi_indices = np.where(roi_data > 0)
        fa_values_in_roi = fa_data[roi_indices]

        voxel_coords = np.column_stack((roi_indices[0], roi_indices[1], roi_indices[2]))
        voxel_data = np.column_stack((voxel_coords, fa_values_in_roi))
    
        region_name = mask.split('.', 1)
        output_name = "voxel_" + region_name[0] + ".csv"

        np.savetxt(output_name, voxel_data, fmt='%d,%d,%d,%f', header='X,Y,Z,FA')
"""
This function takes the filename of the CSV containing the voxels and their corresponding CSV scores, and returns a list of all the voxels with FA scores that are 0, and a dictionary in which the voxels coordinates are the keys, and their scores are the values.

Parameters: csv_filename (str) -> the name of the csv file containing the voxels and scores for a specific region
Returns:
    zero_fa_list: [..., (X, Y, Z), ...] -> list of all the voxels with an FA score of 0
    non_zero_fa_list: {(X, Y, Z): <fa_score>} -> dictionary of voxel coordinates and FA scores of all voxels that have a score greater than 0
Results: Summarized data
"""
def process_voxel_data(csv_filename):
    df = pd.read_csv(csv_filename)

    zero_fa_voxels = df[df['FA'] == 0][['# X', 'Y', 'Z']]
    zero_fa_list = [tuple(x) for x in zero_fa_voxels.to_records(index = False)]

    non_zero_fa_voxels = df[df['FA'] != 0]
    non_zero_fa_list = {tuple(row[['# X', 'Y', 'Z']]): row['FA'] for index, row in non_zero_fa_voxels.iterrows()}
   
    return zero_fa_list, non_zero_fa_list



if __name__ == "__main__":
    files = os.listdir(os.getcwd())

    csv_files = [file for file in files if file.endswith(".csv")]
    
    for csv_filename in csv_files:
        df = pd.read_csv(csv_filename)
        zero_list, non_zero_list = process_voxel_data(csv_filename)

        print(f"{csv_filename}\n\tNumber of Entries: {df.shape[0]}\n\tNumber of Zero Voxels: {len(zero_list)}\n\tNumber of Non-Zero Voxels: {len(non_zero_list.keys())}")


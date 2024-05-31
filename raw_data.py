import nibabel as nib
import numpy as np
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

if __name__ == "__main__":
    

    img_name = "ADNI_003_S_1074_MR_corrected_FA_image_Br_20151030135337354_S256382_I537875_FA_masked_FAskel.nii.gz"
    extract(img_name)

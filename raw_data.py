import nibabel as nib
import numpy as np

if __name__ == "__main__":
    masks = ["cingulum_cingulate_gyrus_L.nii.gz", "cingulum_cingulate_gyrus_R.nii.gz", "cingulum_hippocampus_L.nii.gz", "cingulum_hippocampus_R.nii.gz", "corpus_callosum_body.nii.gz", "corpus_callosum_genu.nii.gz", "corpus_callosum_splenium.nii.gz"]


    fa_img = nib.load("ADNI_003_S_1074_MR_corrected_FA_image_Br_20151030135337354_S256382_I537875_FA_masked_FAskel.nii.gz")


    for mask in masks:
        roi_mask = nib.load(mask)

        fa_data = fa_img.get_fdata()
        roi_data = roi_mask.get_fdata()

        roi_indices = np.where(roi_data > 0)
        fa_values_in_roi = fa_data[roi_indices]

        non_zero_indices = fa_values_in_roi > 0.000001
        filtered_fa_values = fa_values_in_roi[non_zero_indices]
        filtered_voxel_coords = np.column_stack((roi_indices[0][non_zero_indices], roi_indices[1][non_zero_indices], roi_indices[2][non_zero_indices]))

        voxel_data = np.column_stack((filtered_voxel_coords, filtered_fa_values))
    
        region_name = mask.split('.', 1)
        output_name = "voxel_" + region_name[0] + ".txt"

        np.savetxt(output_name, voxel_data, fmt='%d %d %d %f', header='X Y Z FA')



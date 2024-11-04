import nibabel as nib
import numpy as np
import pandas as pd
import os
import csv
"""
This function takes the filename of the brain scan you wish to be analyzed, and returns a CSV file that contains all of the FA scores for the 7 masks found in the directory

Parameters: img_name -> filename of the .nii.gz file. Assumming that the photo has been preprocessed according to TBSS protocols and is ready to be masked.

Returns: None

Results: 7 files containing the FA scores for each voxel in the masked region. voxel_<region>.csv 
"""
def extract(folder):
    cingulum_masks = ["cingulum_cingulate_gyrus_L.nii.gz", "cingulum_cingulate_gyrus_R.nii.gz", "cingulum_hippocampus_L.nii.gz", "cingulum_hippocampus_R.nii.gz"] 
    corpus_masks = ["corpus_callosum_body.nii.gz", "corpus_callosum_genu.nii.gz", "corpus_callosum_splenium.nii.gz"]
    cingulum_data = []
    corpus_data = []

    print("Started Gathering Data")
    for root, dirs, files in os.walk(folder):
        for name in files:
            if name.endswith(('_masked_FAskel.nii.gz')):
                fa_img = nib.load(os.path.join(root, name))

                # Cingulum Data
                cingulum_name_data = []
                cingulum_data_array = np.empty(0)
                cingulum_name_data.append(name.removesuffix('_masked_FAskel.nii.gz'))

                for mask in cingulum_masks:
                    roi_mask = nib.load(mask)

                    fa_data = fa_img.get_fdata()
            
                    roi_data = roi_mask.get_fdata()

                    roi_indices = np.where(roi_data > 0)
                    fa_values_in_roi = fa_data[roi_indices]

                    non_zero_indices = fa_values_in_roi > 0.000001
                    filtered_fa_values = fa_values_in_roi[non_zero_indices]

                    cingulum_data_array = np.concatenate((cingulum_data_array, filtered_fa_values))

                cingulum_name_data = cingulum_name_data + cingulum_data_array.tolist()
                cingulum_data.append(cingulum_name_data)

                # Corpus Data
                corpus_name_data = []
                corpus_data_array = np.empty(0)
                corpus_name_data.append(name.removesuffix('_masked_FAskel.nii.gz'))

                for mask in corpus_masks:
                    roi_mask = nib.load(mask)

                    fa_data = fa_img.get_fdata()
            
                    roi_data = roi_mask.get_fdata()

                    roi_indices = np.where(roi_data > 0)
                    fa_values_in_roi = fa_data[roi_indices]

                    non_zero_indices = fa_values_in_roi > 0.000001
                    filtered_fa_values = fa_values_in_roi[non_zero_indices]

                    corpus_data_array = np.concatenate((corpus_data_array, filtered_fa_values))

                corpus_name_data = corpus_name_data + corpus_data_array.tolist()
                corpus_data.append(corpus_name_data)
    print("Finished Gathering Data")


    print("Writing Cingulum Data")
    with open('ADNI_Cingulum_Data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for line in cingulum_data:
            writer.writerow(line)
    
    print("Writing Corpus Data")
    with open('ADNI_Corpus_Data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for line in corpus_data:
            writer.writerow(line)
        

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
    '''
    files = os.listdir(os.getcwd())

    csv_files = [file for file in files if file.endswith(".csv")]
    
    for csv_filename in csv_files:
        df = pd.read_csv(csv_filename)
        zero_list, non_zero_list = process_voxel_data(csv_filename)

        print(f"{csv_filename}\n\tNumber of Entries: {df.shape[0]}\n\tNumber of Zero Voxels: {len(zero_list)}\n\tNumber of Non-Zero Voxels: {len(non_zero_list.keys())}")
    '''

#extract('ADNI_003_S_4081_MR_corrected_FA_image_Br_20131105134446614_S201678_I397221_masked_FAskel.nii.gz')
#extract('ADNI_003_S_4119_MR_corrected_FA_image_Br_20120421204025212_S142188_I299598_masked_FAskel.nii.gz')
#extract('ADNI_003_S_4119_MR_corrected_FA_image_Br_20130129182512029_S167335_I356961_masked_FAskel.nii.gz')
#extract('C:/Users/myth_/OneDrive/Documents/University/Classes/Summer 2024/Data/Data/Custom/Test File Extract')
extract('//wsl.localhost/Ubuntu/home/cranerm2/Summer2024/enigmaDTI/TBSS/run_tbss/FA_individ')
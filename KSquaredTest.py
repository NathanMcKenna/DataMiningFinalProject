# Author: Maryam Mazadi
# Course: Data Mining
import csv;
import copy


#This function normalizes a set of numbers to a range of 0 and 1, by first shifting them down and then scaling down
# the range.
def Normalize(numbers):
    max_num = max(numbers);
    min_num = min(numbers);
    return [(float(n) - min_num)/(max_num-min_num) for n in numbers]

def normalzie_csv_data(rows):
    ignore_rows = [0,1,13,14,33];
    # transpose the list including the header
    new_rows = zip(*rows);
    col_idx = 0;
    data_normalized = [];
    for row in new_rows:
        # ignore columns that are not numbers
        if(col_idx not in ignore_rows):
            # normalize values, except for the header that is a string
            # remove empty spaces, comma and dollar signs and convert to float
            x = [value.replace("$", "") for value in row[1:]];
            x = [value.replace(",", "") for value in x];
            x  = [float(value) for value in x if value != ''];
            row_normalized = Normalize(x);
            data_normalized.append(row_normalized);
        else:
            data_normalized.append([]);
        col_idx = col_idx + 1;
    return data_normalized;

def categorize_csv_data(data):
    categorized_data = copy.deepcopy(data);
    for r in range(0, len(categorized_data)):
        for c in range(0, len(categorized_data[r])):
            val = categorized_data[r][c];
            if(val < 0.2):
                categorized_data[r][c] = 1;
            elif(val < 0.4):
                categorized_data[r][c] = 2;
            elif(val < 0.6):
                categorized_data[r][c] = 3;
            elif(val < 0.8):
                categorized_data[r][c] = 4;
            else:
                categorized_data[r][c] = 5;
    return categorized_data;

# calculate o_ij at the number of occurances for joing event A=a AND B=b
def count_joint_occurance(list_A, list_B, a, b):
    count = 0;
    for i in range(0, len(list_A)):
        if(list_A[i] == a and list_B[i]==b):
            count = count + 1;
    return count;

if(__name__ == "__main__"):
    # Read CSV data that includes input information
    rows = [];
    with open('finalmerge_cleaned.csv') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            rows.append(row)

    # Normalize all data, except those which are not numbers
    data_normalized = normalzie_csv_data(rows);
    # categoriza data to 5 category
    data_categorized = categorize_csv_data(data_normalized);

    #NOTE: We can use only up to column 17 which is GDP for X2 analysis becasuse there are missing
    # data after this column
    # perform Chi-Squared test between happiness score and other attributes
    print("Procesing Chi - Squared values:");
    happ_idx = 3;
    freedom_idx = 9;
    c = 5; # number of columns is always 5 becasuse we categorized them to 5 categories
    r = 5; # number of rows is always 5 becasuse we categorized them to 5 categories

    for attrib_idx in [6,7,8,9,10,11,12,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]:
        data_A = data_categorized[happ_idx];
        data_B = data_categorized[attrib_idx];
        if(len(data_A) != len(data_B)):
            raise ValueError('Length of properties are not the same!');
        X2 = 0;
        for i in range(1, c+1):
            for j in range(1, r+1):
                e_ij = data_A.count(i) * data_B.count(j) / len(data_A);
                # remove empty categories from calculations
                if(e_ij != 0):
                    o_ij = count_joint_occurance(data_A, data_B, i, j);
                    X2 = X2 + ((o_ij - e_ij)**2)/e_ij;
        print(rows[0][happ_idx], " and ", rows[0][attrib_idx], ", X2: ", X2);

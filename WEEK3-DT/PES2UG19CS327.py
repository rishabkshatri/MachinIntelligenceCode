#RISHAB KSHATRI
#PES2UG19CS327
'''Return Information Gain of the attribute provided as parameter'''
# input:pandas_dataframe,str
# output:int/float
def get_information_gain(df, attribute):                        #FUNCTION TO CALCULATE INFORMATION GAIN
    information_gain = 0
    if df.empty:
        return 0
    elif attribute in df:                                       #USING FORMULA TO CALCULATE IG
        information_gain = get_entropy_of_dataset(df) - get_avg_info_of_attribute(df, attribute)
    return information_gain


'''
Assume df is a pandas dataframe object of the dataset given
'''

import numpy as np
import pandas as pd
import random


'''Calculate the entropy of the enitre dataset'''
# input:pandas_dataframe
# output:int/float
def get_entropy_of_dataset(df):                             #FUNCTION TO GET THE ENTROPY OF THE DATASET
    if df.empty: return 0
    entropy = 0
    classLabel = df.columns[-1]
    uniqueValues = df[classLabel].unique()                  #FINDING THE UNIQUE VALUES TO RUN THAT MANY NO OF TIMES IN FOR LOOP
    # Finds all the unique variables and sorts them as per count
    for value in uniqueValues:
        countOfUnique = df[classLabel].value_counts()[value]
        # Finds count as present in the uniqueValues
        probabilityValue = countOfUnique / len(df[classLabel])
        if probabilityValue == 0: continue
        entropy = entropy - (probabilityValue * np.log2(probabilityValue))
    return entropy                                          #RETURNING ENTROPY CALCULATED


'''Return avg_info of the attribute provided as parameter'''
# input:pandas_dataframe,str   {i.e the column name ,ex: Temperature in the Play tennis dataset}
# output:int/float
def get_avg_info_of_attribute(df, attribute):               #FUNCTION TO GET AVERAGE INFORMATION OF THE DATASET
    if df.empty: return 0
    avg_info = 0
    classLabel = df.columns[-1]
    classLabelValues = df[classLabel].unique()
    if attribute in df:
        attributeValues = df[attribute].unique()
        for value in attributeValues:
            entropyAttribute = 0
            valueOfAttributeMatch = len(df[attribute][df[attribute] == value])
            # Number of times that match the unique values in the column of the attribute. The number of times the certain attribute value is repeated
            for target in classLabelValues:
                numberOfMatch = len(df[attribute][df[attribute] == value][df[classLabel] == target])
                # Number of times that the class label is a certain value and the attribute value is a certain value
                probability = (numberOfMatch / valueOfAttributeMatch)
                # This is the probability that when attribute is A the class label is a certain value
                if probability == 0: continue
                entropyAttribute = entropyAttribute - (probability * (np.log2(probability)))
            avg_info = avg_info + ((valueOfAttributeMatch / len(df[attribute])) * entropyAttribute)
    else:
        return 0  # The attribute is not in the dataset
    return avg_info                                         #RETURNING AVERAGE INFORMATION OF THAT COLUMN

#input: pandas_dataframe
#output: ({dict},'str')
def get_selected_attribute(df):
    '''
    Return a tuple with the first element as a dictionary which has IG of all columns
    and the second element as a string with the name of the column selected

    example : ({'A':0.123,'B':0.768,'C':1.23} , 'C')
    '''
    df2 = df
    if df.empty or len(df.columns) == 1:
        return (dict(), '')
    Dictionary = dict()
    df2 = df2.iloc[:, :-1]
    # Removing the last column from the dataframe
    listOfAttributes = list(df2)
    selectedNode = ''
    selectedNodeInfoGain = 0
    # Getting all the attributes and leaving out just the last column which consists of just the classlabels
    for attribute in listOfAttributes:
        informationGainOfAttribute = get_information_gain(df, attribute)
        Dictionary[attribute] = informationGainOfAttribute
        if informationGainOfAttribute > selectedNodeInfoGain:
            selectedNode = attribute
            selectedNodeInfoGain = informationGainOfAttribute
    return (Dictionary, selectedNode)

#RISHAB KSHATRI
#PES2UG19CS327
#WEEK 3

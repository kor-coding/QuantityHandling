import pandas as pd


##############################################################################
#
# First peel outer layer, take out an element a time. 
# Then, serialize list of dict into normal dict. 
# Then, convert with new numbering and append into new dict. 
# Then, further serialize multiple lists of dict into normal nested dict. 
# Lastly, do the same thing again for next element until all elements does.
#
# Copyright 2022 - 2023, Chew Siak Kor, siakkor.chew@gmail.com
#

################## Data Laundrying Section ####################

def data_laundry_func(pre_data):
    i = 0
    Laundry_prop = {}
    while i < len(pre_data):
        def outer_data(data):
            outer_set = {}
            for k, v in enumerate(data):
                outer_set[k]=v
            return outer_set
        compile_dict = outer_data(pre_data[i])
        def prop_serializer(data):
            tempData = {}
            for k,v in enumerate(data['properties']):
                if type(v) is list:
                    tempDict = dict()
                    for index, value in enumerate(list):
                        tempDict[index] = value
                    return tempDict
                else:
                    tempData[k]=v
            return tempData
        properties_dict = prop_serializer(pre_data[i])
        #print(properties_dict)
        def change_num(dict1,dict2):
            a = len(dict1)
            i = 0
            while i < len(dict2):
                dict2[i+a]=dict2.pop(i)
                i += 1
        change_num(compile_dict,properties_dict)
        temp_dict = {**compile_dict, **properties_dict}
        #print(temp_dict)
        data_frame = pd.DataFrame.from_dict(temp_dict, orient='index')
        #print(data_frame)
        def data_frame_serializer(data_frame):
            tempData = {}
            i = 6
            j = 0
            while i < len(data_frame):
                for k,v in enumerate(data_frame[0][i]['items']):
                    if type(v) is list:
                        tempDict = dict()
                        for index, value in enumerate(list):
                            tempDict[index] = value
                        return tempDict
                    else:
                        tempData[j]=v
                        j += 1
                i += 1
            else:
                return tempData
        items_dict = data_frame_serializer(data_frame)
        #print(items_dict)
        change_num(compile_dict,items_dict)
        compile_dict.update(items_dict)
        #print(compile_dict)
        Laundry_prop[i] = compile_dict
        i += 1
    return Laundry_prop

################ Data Laundrying Section Ends ##################


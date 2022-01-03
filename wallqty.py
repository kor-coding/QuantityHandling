import json


##############################################################################
#
# Taken from the laundry data, where data source is now all dict and enumerated. 
# First flip the dict as value to key, key to value, to enable use of match function to search keyword. 
# Upon finding keyword, then uses iter_func to determine the correct number of those matched item. 
# Then compose them into a new list. Lastly, summing up the value of the list.
#
# Copyright 2022, Chew Siak Kor, siakkor.chew@gmail.com
#

################## Universal Functions ####################
##### Dict Flipper #####
def dict_flipper(d, seen = []):
    for a, b in d.items():
        if not isinstance(b, dict):
            yield {b:seen+[a]}
        else:
            yield from dict_flipper(b, seen+[a])

##### Iteration Function #####
def iter_func(iterObj,checkerValue,returnValue):
    list_key = []
    while True:
        try:
            element = next(iterObj)
            x = json.dumps(element)
            y = json.loads(x)
            list_key.append(y[checkerValue][returnValue])
        except StopIteration:
            break
    return list_key

##### Compose New Dictionary #####
def compose_new_dict(listKeys,dictSource):
    tempDataSet = {}
    i = 0
    while i < len(listKeys):
        x = listKeys[i]
        y = dictSource[x]
        tempDataSet[x] = y
        i += 1
    return tempDataSet

##### Quantity List (for Sum Use with 3 keys) #####
def qty_list(dictSource,listSource1,listSource2):
    float_list = []
    i = 0
    while i < len(listSource1):
        a = dictSource[listSource1[i]][listSource2[i]]['value']
        b = float(a)
        float_list.append(b)
        i += 1
    return float_list

"""
##### Quantity List (for Sum Use with 3 keys) #####
def qty_list(dictSource,listSource1,listSource2,listSource3):
    float_list = []
    i = 0
    while i < len(listSource1):
        a = dictSource[listSource1[i]][listSource2[i]][listSource3[i]]['value']
        b = float(a)
        float_list.append(b)
        i += 1
    return float_list
"""


def wallqty(processProp):
    ################## Wall Classifier Section ####################
    """
    WARNING: Do not quote this entire section as a function!
    This section should run as soon as getting the data!
    Not supposed to be activated!
    """
    wall_checker = 'IfcWallStandardCase'
    #bi_check_wall = 'Non-bearing'
    ##### Dict Flipper #####
    wallDictInvertedList = list(dict_flipper(processProp))
    wall_matches = [match for match in wallDictInvertedList if wall_checker in match]
    wall_iter_obj = iter(wall_matches)
    ##### Iteration Function #####
    wall_keySet = iter_func(wall_iter_obj,wall_checker,0)
    # Remove '#' only when needs for error checking
    #print(wall_keySet)
    #### Wall Classifier First Section Ends ####
    #### Can Jump Shift to 'for i in wall_keySet' ####
    """
    ##### Compose New Dictionary #####
    wall_bicheck_dictionary = compose_new_dict(wall_keySet,processProp)
    ##### Dict Flipper #####
    wall_bicheck_dictInvertedList = list(dict_flipper(wall_bicheck_dictionary))
    wall_bicheck_matches = [match for match in wall_bicheck_dictInvertedList if bi_check_wall in match]
    wall_bicheck_iter_obj = iter(wall_bicheck_matches)
    ##### Iteration Function #####
    wall_bicheck_keySet = iter_func(wall_bicheck_iter_obj,bi_check_wall,0)
    # Remove '#' only when needs for error checking
    #print(wall_bicheck_keySet)
    """
    for i in wall_keySet:
        processProp[i]['OmniClass'] = {'22-04 21 13 ':'Brick Masonry '}
    # Remove '#' only when needs for error checking
    #print(data[0]['OmniClass'])
    #print(data[2]['OmniClass'])
    ################ Wall Classifier Section Ends ################
    ################## Wall Quantity Section ####################
    brickwall_quantity_type = 'Area'
    #generate quantity dictionary using final checked keySet (wall_bicheck_keySet for wall)
    ##### Compose New Dictionary #####
    wall_quantity_dict = compose_new_dict(wall_keySet,processProp)
    ##### Dict Flipper #####
    wall_quantity_dictInvertedList = list(dict_flipper(wall_quantity_dict))
    wall_quantity_matches = [match for match in wall_quantity_dictInvertedList if brickwall_quantity_type in match]
    wall_quantity_iter_obj = iter(wall_quantity_matches)
    ##### Iteration Function #####
    wall_qty_2nd_key = iter_func(wall_quantity_iter_obj,brickwall_quantity_type,1)
    # Remove '#' only when needs for error checking
    #print(wall_qty_2nd_key)
    """
    ### weird... there's a need of repeat the whole set then only able to generate 3rd key with the exact same code
    ##### Compose New Dictionary #####
    key3_wall_quantity_dict = compose_new_dict(wall_keySet,processProp)
    ##### Dict Flipper #####
    key3_wall_quantity_dictInvertedList = list(dict_flipper(key3_wall_quantity_dict))
    key3_wall_quantity_matches = [match for match in key3_wall_quantity_dictInvertedList if brickwall_quantity_type in match]
    key3_wall_quantity_iter_obj = iter(key3_wall_quantity_matches)
    ##### Iteration Function #####
    wall_qty_3rd_key = iter_func(key3_wall_quantity_iter_obj,brickwall_quantity_type,2)
    # Remove '#' only when needs for error checking
    #print(wall_qty_3rd_key)
    """
    ##### Quantity List (for Sum Use) #####
    wall_qty_list = qty_list(processProp,wall_keySet,wall_qty_2nd_key)
    total_wall_qty = sum(wall_qty_list)
    ################ Wall Quantity Section Ends ################
    return total_wall_qty
import json

from django.shortcuts import render
from django.http import JsonResponse

from .dict import Omni
from .wallqty import wallqty
from .slabconcqty import slabconcqty
from .beamconcqty import beamconcqty
from .columnconcqty import columnconcqty
from .Laundry import data_laundry_func

##############################################################################
#
# DataHandling – processor
# First json.load the data from an AJAX POST request
# Then, extract specifically “data” data source. 
# Pass the extracted data source into laundry to make possible use of data source. 
# Based on the laundry processed data source, extract quantities to each different bill item. 
# Compile extracted bill item quantities into OmniClass, MYSMM3, or even any other BQ required item type and structure. 
# Lastly compose it all into a brand new nested dict.
#
# Copyright 2022, Chew Siak Kor, siakkor.chew@gmail.com
#

def processor(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Get requested data and create data dictionary
        #Do something with the data from the POST request
        modelProperties = json.load(request)
        properties = modelProperties['data']
        laundry_data = data_laundry_func(properties)
        get_wall_qty = wallqty(laundry_data)
        get_slab_conc_qty = slabconcqty(laundry_data)
        get_beam_conc_qty = beamconcqty(laundry_data)
        get_column_conc_qty = columnconcqty(laundry_data)
        qty_dict = {}
        def WallQty(qty):
            if qty is None:
                Wall = None
            else:
                Wall = {
                    "OmniClass":{
                        "SN":"22-04 21 13",
                        "desc":"Brick Masonry",
                        "unit":"m2",
                        "qty":qty,
                        "rate":40.00
                        },
                    "MYSMM3":{
                        "SN":"11-01 01 01",
                        "desc":"Half brick (115mm thick) wall common clay brick",
                        "unit":"m2",
                        "qty":qty,
                        "rate":40.00
                        },
                }
            return Wall
        qty_dict["Wall"] = WallQty(get_wall_qty)

        def SlabConcQty(qty):
            if qty is None:
                Slab = None
            else:
                Slab = {
                    "OmniClass":{
                        "SN":"22-03 00 00",
                        "desc":"Concrete",
                        "unit":"m3",
                        "qty":qty,
                        "rate":280.00
                        },
                    "MYSMM3":{
                        "SN":"09-01 02 06",
                        "desc":"Vibrated reinforced in-situ concrete in slabs",
                        "unit":"m3",
                        "qty":qty,
                        "rate":280.00
                        },
                }
            return Slab
        qty_dict["Slab Conc"] = SlabConcQty(get_slab_conc_qty)

        def BeamConcQty(qty):
            if qty is None:
                Beam = None
            else:
                Beam = {
                    "OmniClass":{
                        "SN":"22-03 00 00",
                        "desc":"Concrete",
                        "unit":"m3",
                        "qty":qty,
                        "rate":280.00
                        },
                    "MYSMM3":{
                        "SN":"09-01 02 09",
                        "desc":"Vibrated reinforced in-situ concrete in beams",
                        "unit":"m3",
                        "qty":qty,
                        "rate":280.00
                        },
                }
            return Beam
        qty_dict["Beam Conc"] = BeamConcQty(get_beam_conc_qty)

        def ColumnConcQty(qty):
            if qty is None:
                Column = None
            else:
                Column = {
                    "OmniClass":{
                        "SN":"22-03 00 00",
                        "desc":"Concrete",
                        "unit":"m3",
                        "qty":qty,
                        "rate":280.00
                        },
                    "MYSMM3":{
                        "SN":"09-01 02 11",
                        "desc":"Vibrated reinforced in-situ concrete in columns",
                        "unit":"m3",
                        "qty":qty,
                        "rate":280.00
                        },
                }
            return Column
        qty_dict["Column Conc"] = ColumnConcQty(get_column_conc_qty)

        return JsonResponse(qty_dict)
    else:
        #form = InputForm()
        return render(request, 'index.html')

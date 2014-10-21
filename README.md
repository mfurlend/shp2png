shp2png
=======

Creates a `.png` image from a shapefile.
By default it will draw all polygons in the shapefile.
You can specify which polygon you want to draw by providing
an `attribute filter`. 

Attribute filters can be chained.

The syntax for an attribute filter is as followed:
`
python shp2png.py <SHAPEFILE NAME> -f <ATTRIBUTE NAME> "<ATTRIBUTE VALUE>" -f <SECOND ATTRIBUTE NAME> "<SECOND ATTRIBUTE VALUE>" -o <OUTPUT NAME>
`

You can batch-generate multiple images by specifying a `group by` constraint.
Group by constraints look like attribute filters, 
but are surrounded by [square brackets] and do not have attribute values.

The syntax for a "group by" constraint is as followed:

`
python shp2png.py <SHAPEFILE NAME> -f [<ATTRIBUTE NAME>] -o <OUTPUT PREFIX>
`

The polygon fill and stroke colors are white by default. 
You can override the colors with the `--fill` and `--stroke` options respectively.

To generate an additional image with a transparent polygon and opaque stroke specify the `--outline` option.
`--outline` takes an optional color parameter (defaults to black):

    --outline rgb(255,0,0)
    or
    --outline red


The default image width is `4333` (pixels). 
You can override this with the `--width` option.

Example output (without attribute filters):
![Example image without attribute filters](https://cloud.githubusercontent.com/assets/1995161/4720275/eb189408-592f-11e4-9163-4f6f7757aaf9.png)


This script requires the Python Imaging Library. 
To to install it run `pip install PIL` or `easy_install PIL`

 author: Mike Furlender
 date: 20140910

  mfurlend AT gmail DOT com

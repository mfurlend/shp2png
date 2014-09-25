shp2png
=======

shp2png.py - Creates a `.png` image from a shapefile.
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

The default image width is `4333` (pixels). 
You can override this with the `--width` option.

author: mfurlend AT gmail DOT com
date: 20140910

This script requires the Python Imaging Library.

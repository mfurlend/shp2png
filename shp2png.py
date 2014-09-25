import shapefile, sys
import Image, ImageDraw
import argparse

parser = argparse.ArgumentParser(description="Produce .png image from shapefile. Optionally filter by attribute value(s).")

parser.add_argument('input' ,help='input filename (without .shp)')
parser.add_argument('-o','--output', required=True, help='output filename (without .png)')
parser.add_argument('-w', '--width', type=int, default=4333)
parser.add_argument('--fill', type=str, default='rgb(255, 255, 255)', help="polygon fill color. defaults to \"rgb(255, 255, 255)\"")
parser.add_argument('--stroke', type=str, default='rgb(255, 255, 255)', help="polygon stroke color. defaults to \"rgb(255, 255, 255)\"")
parser.add_argument('--outline', type=str, nargs="?", default=False, help="show outline. takes optional color parameter. defaults to \"rgb(0, 0, 0)\"")
parser.add_argument('-f',  '--filter', nargs='*', action='append', default=[], help='include features matched by this key-value pair')

args = vars(parser.parse_args())

if args['outline'] == None:
  args['outline'] = 'rgb(0, 0, 0)'
  
myshp = open(args['input']+".shp", "rb")
mydbf = open(args['input']+".dbf", "rb")
r = shapefile.Reader(shp=myshp, shx=None, dbf=mydbf)
iwidth = args['width']
# end if

filter_idxs = []
groupby_idxs = []
if len(args['filter']):
  filter_keys = [x[0] for x in args['filter'] if x[0][0] != '[']
  groupby_keys = [x[0][1:-1] for x in args['filter'] if x[0][0] == '[']
  vals = [x[1] for x in args['filter'] if x[0][0] != '[' ]
  fields=[y[0] for y in r.fields]
  filter_idxs =[fields.index(x)-1 for x in filter_keys if x in fields]
  groupby_idxs =[fields.index(x)-1 for x in groupby_keys if x in fields]
  if len(groupby_idxs) >0: #group by active
    group_bys = list(set([x[y] for x in r.records() for y in groupby_idxs if x[y].replace(' ','') != ''])) #unique values in group by clause
  else:
    group_bys = ['']
  # end if  
# end if


for group_by in group_bys:
  feature_counter = 0
  if group_by != '':
    sys.stdout.write ("group by "+group_by +'.....')
  xys=[]
  boxes = [] 
  for sr in r.shapeRecords():    
    if len(filter_idxs)>0:
      n = len([i for i,x in enumerate(filter_idxs) if sr.record[x]==vals[i]])
      if n ==0:
        continue
      # end if
    # end if
    if group_by != '':
      n = len([i for i,x in enumerate(groupby_idxs) if sr.record[x]==group_by])
      if n ==0:
        continue
      # end if
    # end if
    feature_counter = feature_counter + 1
    shape=sr.shape
    boxes.append(shape.bbox)
    xy = []
    for x,y in shape.points:  
      xy.append((x,y))
    xys.append(xy) 
  
  print "features: "+str(feature_counter)  
  nbbox = boxes[0]
  
  for bbox in boxes:
    if bbox[2] > nbbox[2]:
    # end if
    
      nbbox[2] = bbox[2]
    # end if
    
    if bbox[3] > nbbox[3]:
    # end if
    
      nbbox[3] = bbox[3]
    # end if
    
    if bbox[0] < nbbox[0]:
    # end if
    
      nbbox[0] = bbox[0]
    # end if
    
    if bbox[1] < nbbox[1]:
    # end if
    
      nbbox[1] = bbox[1]
    # end if
  # end for
    


  bbox=nbbox
  xdist = bbox[2] - bbox[0]
  ydist = bbox[3] - bbox[1]
  ratio=xdist/ydist
  iheight = int(iwidth/ratio)
  xratio = iwidth/xdist
  yratio = iheight/ydist

  img = Image.new("RGB", (iwidth, iheight), "white")
  img2 = Image.new("RGB", (iwidth, iheight), "white")
  transparent_area = (0,0,iwidth,iheight)

  mask=Image.new('L', (iwidth, iheight), color=255)
  draw=ImageDraw.Draw(mask) 
  draw.rectangle(transparent_area, fill=0)
  img.putalpha(mask)
  img2.putalpha(mask)

  draw = ImageDraw.Draw(img)
  draw2 = ImageDraw.Draw(img2)

  for pts in xys:
    pixels2 = []
    for x,y in pts:
      px = int(iwidth - ((bbox[2] - x) * xratio))
      py = int((bbox[3] - y) * yratio)
      pixels2.append((px,py))
    draw.polygon(pixels2, outline=args['stroke'], fill=args['fill'])
    if args['outline'] != False:
      draw2.polygon(pixels2, outline=args['outline'])

    
  img.save(args['output']+"_"+group_by+"_polygon.png")
  if args['outline'] != False:
    img2.save(args['output']+"_"+group_by+"_lines.png")
  # end if


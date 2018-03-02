import scipy, numpy
from scipy.spatial.distance import pdist, squareform  

def merge_points(x,y,z,r):
  # Compute distance matrix 
  n = len(x);
  XY = numpy.ndarray(shape = (n,2), dtype = float)
  for i in range(0,n):
    XY[i,0] = x[i]
    XY[i,1] = y[i]
  D = scipy.spatial.distance.pdist(XY, 'sqeuclidean')
  ix = numpy.where(D < r*r)
  rc = vec_row_col(n,ix[0])

  if len(rc) == 0: print "... merging complete with", n, "data points"; return 1
  else:  print "...", len(rc), "pairs of close points"
 
  # Make a list of point groups 
  cl=[]; groups=[]
  pairs=list(rc)
  cl.append(pairs[0])
  
  if len(pairs) == 1:
    groups.append(cl)

  for i in range(1,len(pairs)):
      if pairs[i][0] == pairs[i-1][0]:
         cl.append(pairs[i])
      else:
         groups.append(cl) 
         cl=[]
         cl.append(pairs[i])
  # Compute centroids and mark points for deletion
  cent_x=[]; cent_y=[]; cent_z=[]; g_i=[True]*n; i_done=[False]*n;
  xx=[]; yy=[]; zz=[]
  for i in range(0,len(groups)):
      ii=groups[i][0][0]
      div = 1
      if i_done[ii]:
        continue
      else:
        div = 1 
        cx = x[ii]; cy = y[ii]; cz = z[ii]
        g_i[ii]=False; i_done[ii]=True
      for j in range(0,len(groups[i])):
        ij=groups[i][j][1]
        if i_done[ij]:
          g_i[ii]=True  
        else:
          div += 1
          cx += x[ij]; cy += y[ij]; cz += z[ij]
          g_i[ij]=False; i_done[ij]=True
      cent_x.append(cx/div); cent_y.append(cy/div); cent_z.append(cz/div)
  # Delete points and replace them with centroids
  for i in range(0,n):
    if g_i[i]:
      xx.append(x[i]); yy.append(y[i]); zz.append(z[i])
  x = xx[:]; y = yy[:]; z = zz[:]
  x += cent_x; y += cent_y; z += cent_z
  return(x,y,z)

def sq2cond(i, j, n):
    assert i != j, "no diagonal elements in condensed matrix"
    if i < j:
        i, j = j, i
    return n*j - j*(j+1)/2 + i - 1 - j
def vec_row_col(d,i):                                                               
  b = 1 - 2* d
  x = (numpy.floor((-b - numpy.sqrt(b*b - 8*i))*0.5)).astype(int)
  g = (i + x*(b + x + 2)*0.5 + 1).astype(int)
  if i.shape:                                                                     
    return zip(x,g)                                                             
  else:                                                                           
    return (x,g) 
def sqdistance(p1,p2):
  import math
  sqd = (x[p1]-x[p2])*(x[p1]-x[p2]) + (y[p1]-y[p2])*(y[p1]-y[p2]) 
  return sqd

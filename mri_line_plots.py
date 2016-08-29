
# coding: utf-8

# In[7]:

# Import packages and modules
#-----------------------------------------------------------
# Read a dicom series using pydicom
import os
#print os.getcwd() # print current working dir as a sanity check
import dicom
import numpy
from matplotlib import pyplot, cm # from matplotlib, import pyplot (plotting framework) and cm (colourmap) modules
import pylab # 
from natsort import natsorted
get_ipython().magic(u'matplotlib inline')
# ensures output of matplotlib (i.e. plots) is displayed inline in the notebook
# The next bit of code uses os.path.walk to traverse the 'MyHead' directory,
# and collect all .dcm files into a list named lstFilesDCM #
#-----------------------------------------------------------

#---------------------------------------
# locate and define working dir and files/ paths of interest

PathDicom = "/home/tempie/analysis/test_pydicom/5/test_rename_4/" # define working dir explicitly
lstFilesDCM = []  # create an empty list,

for dirName, subdirList, fileList in os.walk(PathDicom,topdown=True):
    # From os module, apply 'walk'method
    # walk generates the filenames in a directory tree by 'walking' the tree
    # os.walk usage: define variables dirName, subdirList, fileList. Read through working dir 'PathDicom'
    fileList.sort() # important to sort list into sensible order
    for filename in fileList: # for counter filename, work through filelst 
        # print fileList # fileList is a list of all files in the dir named 'PathDicom'
        # aside, dirName and PathDicom (above) are the same
        # print dirName # This will print dirName (i.e. path to dicom dir)
        # Note, this is the same as PathDicom
        #print filename.lower() # This will print list 'filename' in lower case
        if ".dcm" in filename.lower():  # make files lower case then check whether the file's DICOM
            # I.e. only include (list) .dcm files in the list of filenames lstFilesDCM
            # Append to list, the full path and filenames of all dicom files
            lstFilesDCM.append(os.path.join(dirName,filename))
# print lstFilesDCM # This will print the full path and filename of all *.dcm files in the working dir
# print fileList # fileList is a list of all files in the dir named 'PathDicom'

#----------------------------------------------
#============================================
# This little section determines the number of files in the array, calculates the position of the middle file
# then lists the middle item of the array
# print RefDs
totnumslices = len(lstFilesDCM) # Prints the size of the array 'lstFilesDCM' i.e. the number of the filenames in this case
# print totnumslices
midslice =totnumslices/2
# print midslice
# lstFilesDCM[midslice]
# See also list.index(object), may be useful for similar purposes
#============================================
#=================================================


# The next section of the code uses pydicom A notable aspect of this package is that upon reading 
# a DICOM file, it creates a dicom.dataset.FileDataset object where the 
# different metadata are assigned to object attributes with the same name.
# The dicom header will be read. RefDs
# Then the image pixel dimensions will be determined
# Then the image pixel spacing (pixel size) will be determined, assumes no slice gap

# Read 1st file metadata i.e. dicom header info, will be used later to get info about the image

#===========
# The following reads the slice number in order of the slice order as seem by the list above into a list of strings
RefDs = dicom.read_file(lstFilesDCM[0])
truesliceorderlist = []
for count in range (0,len(lstFilesDCM)):
    truesliceorderlist.append(dicom.read_file(lstFilesDCM[count]).InstanceNumber) # square brackets make it a list? array
# print truesliceorderlist
#==============
# The following zero pads the list of strings using the values fro the list above
# Modify the items of the list to zero pad names and add .dcm extension
# This will work for dicom directories with up to 100000 images
# Note that this script does not consider 4D dicom data i.e. EPI (fMRI, DTI) based sequences
padded_array = ["{:05d}.dcm".format(item) for item in truesliceorderlist]
# print padded_array
# padded_array_append_dcm = 
#y = len(truesliceorderlist)
#print y

#=====
# Now rename files using the two sets of lists I have above i.e. rename each element of a list 
# for the total number of slices 
# Remarkably this works as an example of how to rename a list of files in python
os.path.abspath('/home/tempie/analysis/test_pydicom/5/test_rename_4')
os.chdir('/home/tempie/analysis/test_pydicom/5/test_rename_4')
# !pwd
for rename in range (0,len(lstFilesDCM)):
    os.rename(fileList[rename], padded_array[rename])
#===================


# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
# print ConstPixelDims
# print RefDs.Rows # prints output from DICOM header 'Rows' i.e. 0028, 0010 
# print RefDs.Columns # prints output from DICOM header 'Columns' i.e. 0028, 0011
# print len(lstFilesDCM) # prints length of array i.e. # of files equivalent to # of slices
# Therefore ConstPixelDims has been defined

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))
# print ConstPixelSpacing 
# print RefDs.PixelSpacing # prints output from DICOM header 'Pixel spacing' i.e. 0028, 0030, element 0
# print RefDs.PixelSpacing # prints output from DICOM header 'Pixel spacing' i.e. 0028, 0030, element 1
# print RefDs.SliceThickness # prints output from DICOM header 'Slice thickness' i.e. 0018, 0050, element 1


#============================================================

# From the values derived from the metadata (RefDs) above we
# then use numpy to calculate the dimensions of the 3D numpy array
# Use Numpy arrange to calculate axes for the array
# usage for numpy.arange as follows: arange([start,] stop[, step,], dtype=None)

x = numpy.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = numpy.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = numpy.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])

# where 0.0 is the 'start', the end value is the product of the pixeldim and pixel spacing i.e. the FOV,
# where we add 1 to the pixel dims to account for '0' and ConstPixelSpacing defines the step i.e. pixel width
# print x
# len(x)

#===============================================================

# first create a NumPy array named ArrayDicom with zeros
# This is ditinct from the array dimensions defined above

# The array is sized based on 'ConstPixelDims'
# Usage of numpy.zeros :Return a new array of given shape and type, filled with zeros.
# zeros(shape, dtype=float, order='C')

ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)
# ConstPixelDims defines the shape of the array, dtype

# Thus we have a array dimentions and an array of zeros

# print ArrayDicom.size # This will calc the total number of elements in an array, i.e. the product 
# of the array dimensions

#==================================================================
# What follows is how we populate the zero array above with dicom intensity values using ds.pixel_array
# The array is created by reading the pixel values into the array with ds.pixel_array

PathDicom = "/home/tempie/analysis/test_pydicom/5/test_rename_4/" # define working dir explicitly

lstFilesDCM = []  # create an empty list,

for dirName, subdirList, fileList in os.walk(PathDicom,topdown=True):
    # From os module, apply 'walk'method
    # walk generates the filenames in a directory tree by 'walking' the tree
    # os.walk usage: define variables dirName, subdirList, fileList. Read through working dir 'PathDicom'
    fileList.sort()
    for filename in fileList: # for counter filename, work through filelst 
        # print fileList # fileList is a list of all files in the dir named 'PathDicom'
        # aside, dirName and PathDicom (above) are the same
        # print dirName # This will print dirName (i.e. path to dicom dir)
        # Note, this is the same as PathDicom
        #print filename.lower() # This will print list 'filename' in lower case
        if ".dcm" in filename.lower():  # make files lower case then check whether the file's DICOM
            # I.e. only include (list) .dcm files in the list of filenames lstFilesDCM
            # Append to list, the full path and filenames of all dicom files
            lstFilesDCM.append(os.path.join(dirName,filename))

# loop through all the DICOM files again, now that they are in sensible order
for filenameDCM in lstFilesDCM:
    # read the filenames from the list of paths to dicom and filenames into the pydicom object 'ds'
    ds = dicom.read_file(filenameDCM)
    # For each filenameDCM i.e. each dicom file, read in all file information, metadata and intensity values
    # store the raw image data in the dicom object ds
    # below extracts the pixel info into the array 'ArrayDicom'
    # i.e. reads the pydicom array into the numpy array
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array
    # .index in the context of a python list means the following
    # The method index() returns the lowest index in list that obj appears.
    # i.e. list.index(obj), will return the 'position' of the filename in the list 
    # in this case, this equates to the slice number, defining the 3rd axes of the array
    # i.e. will read 2d pixel data into ArrayDicom, then move onto next slice and repeat
    # print ds.pixel_array
    # print ds.pixel_array.shape
    # pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
    # pylab.show()
# ds or dataset is the base object in the pydicom model
# print filenameDCM
# dicom.read_file?
# USAGE : dicom.read_file(fp, defer_size=None, stop_before_pixels=False, force=False)
# print ds.pixel_array
# print ArrayDicom[1,1,1]
#==============================
# Print summary of image info

# print ConstPixelDims 
# print ConstPixelSpacing

#================================
# Display image using pyplot module from matplotlib 

pyplot.figure(dpi=300) # Creates a new figure with resolution dpi = 300
pyplot.axes().set_aspect('equal', 'datalim') # Set aspect ratio of figure
# 'equal' means same scaling from data to plot units for x and y
# 'datalim' means change xlim or ylim
pyplot.set_cmap(pyplot.gray()) # Set the default colourmap, cmap colourscale 'pyplot.gray()' used in this case
pyplot.pcolormesh(x, y, numpy.flipud(ArrayDicom[:, :, midslice])) # Plot a quadrilateral mesh, show slice 'midslice'
# Where midslice is defined above
# Note the array has been flipped in the up/down direction
pyplot.show() # Display the figure
# Need to add this line to 'show' image
# ==============================


# In[125]:

#===========================
# Reduce the 3D array to a 2D array by extracting the array representing the middle slice of the image
#print ArrayDicom.shape
#print ArrayDicom.size
midslice_array =[] # create a new empty array 
# Note that 'midslice' was calculated earlier
midslice_array = ArrayDicom[:,:,midslice] # reduce my 3D array to a 2D array based on middle slice of image
# print midslice_array.shape
# print midslice_array

#=====================================
# Estalish the shape (size) of the array 'midslice_array'
# Then determine the position of the middle coloum and middle row of the array i.e. at the middle voxel
slice_array_shape = midslice_array.shape
no_of_cols = slice_array_shape[1]
middle_col = no_of_cols/2
#print no_of_cols
#print middle_col
no_of_rows = slice_array_shape[0]
middle_row = no_of_rows/2
#print no_of_rows 
#print middle_row

#======================================
# Reduce the 2D array to a 1d array where the 1D array consists of the intensities from the middle column
# of the image
midcol_array =[] # create an exmpty array named midcol_array
midcol_array = midslice_array[:,middle_col] # create a new 1D array that consists 
# of intensity values from middle column of 2D array
# print midcol_array
#print midcol_array.size
# print midcol_array.shape
#=======================================
#======================================
# Reduce the 2D array to a 1d array where the 1D array consists of the intensities from the middle row
# of the image
midrow_array =[] # create an exmpty array named midcol_array
midrow_array = midslice_array[middle_row,:] # create a new 1D array that consists 
# of intensity values from middle column of 2D array
# print midrow_array
#print midrow_array.size
# print midrow_array.shape
#=======================================
# plot column data
# Plot column as a bar graph
figure1 = pyplot.figure()
y_pos1 = numpy.arange(len(midcol_array)) # Defines the # of data entries in the y-axis i.e. the length of the array
pyplot.bar(y_pos1,midcol_array) # plot the voxel # array vs intensity value array
# pyplot.xticks(y_pos, bins)
pyplot.ylabel('Intensity (ArbU)') # set y-axis label
pyplot.xlabel('Voxel position') # set x-axis label
pyplot.title('Midslice, Midcolumn, Intensity vs. Voxel Position') # set title of graph
pyplot.show()

#=======================================
# plot row data
# Plot row data as a bar graph 
figure2 = pyplot.figure()
y_pos2 = numpy.arange(len(midrow_array)) # Defines the # of data entries in the y-axis i.e. the length of the array
pyplot.bar(y_pos2,midrow_array) # plot the voxel # array vs intensity value array
# pyplot.xticks(y_pos, bins)
pyplot.ylabel('Intensity (ArbU)') # set y-axis label
pyplot.xlabel('Voxel position') # set x-axis label
pyplot.title('Midslice, Midrow, Intensity vs. Voxel Position') # set title of graph
# pyplot.show()
#==========================================

# Alternatively Plot column as a line graph
figure3 = pyplot.figure()
y_pos3 = numpy.arange(len(midcol_array)) # Defines the # of data entries in the y-axis i.e. the length of the array
pyplot.ylabel('Intensity (ArbU)') # set y-axis label
pyplot.xlabel('Voxel position') # set x-axis label
pyplot.title('Midslice, Midcolumn, Intensity vs. Voxel Position') # set title of graph
pyplot.plot(y_pos3,midcol_array)

# Alternatively Plot row as a line graph
figure4 = pyplot.figure()
y_pos4 = numpy.arange(len(midrow_array)) # Defines the # of data entries in the y-axis i.e. the length of the array
pyplot.ylabel('Intensity (ArbU)') # set y-axis label
pyplot.xlabel('Voxel position') # set x-axis label
pyplot.title('Midslice, Midrow, Intensity vs. Voxel Position') # set title of graph
pyplot.plot(y_pos4,midrow_array)
#============================================



# In[ ]:




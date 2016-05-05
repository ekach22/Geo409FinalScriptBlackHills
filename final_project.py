#Build layers for Final Project

import arcpy
arcpy.env.overwriteOutput = True
print "Final Project begins now\n Start building code"

#Declare Variables
infc_workspace = r'T:\users\Ekach\Final_Project\fc'
outgdb_workspace = r'T:\users\Ekach\Final_Project\workspace.gdb'
extent = r'T:\users\Ekach\Final_Project\area_of_interest\workspace.gdb\area_of_interest'
sr = arcpy.SpatialReference(26913)
rasterworkspace = r'T:\users\Ekach\Final_Project\raster'

#Working on feature classes

arcpy.env.workspace = infc_workspace
fclist = arcpy.ListFeatureClasses()

print fclist

for fc in fclist:
	#print fclist
	desc = arcpy.Describe(fc)
	fields = arcpy.ListFields(fc)
	crs = desc.SpatialReference
	print "{0} is a shapetype {1}\n with a CRS {2}".format(desc.basename,desc.shapetype,crs.name)
	#for field in fields:
		#print "Field {0} is of type {1} and length {2}\n".format{field.name,field,type,field.length}
	out_dataset = outgdb_workspace + "/temp" 
	arcpy.Project_management(fc, out_dataset, sr)
	out_clip = outgdb_workspace + "/" + desc.basename.replace(" ", "_")
	arcpy.Clip_analysis(out_dataset, extent, out_clip)
	arcpy.Delete_management(out_dataset)

arcpy.env.workspace = outgdb_workspace
fclist = arcpy.ListFeatureClasses()
	
print fclist

for fc in fclist:
    #print fclist
    desc = arcpy.Describe(fc)
    field = arcpy.ListFields(fc)
    crs = desc.SpatialReference
    print "{0} is a shapetype {1}\n with a CRS {2}".format(desc.basename,desc.shapeType,crs.name)
    for field in fields:
        print "Field {0} is of type {1} and length {2}\n".format(field.name,field.type,field.length)
    
    print crs.name
	
#Set workspace to pull rasters from
arcpy.env.workspace = rasterworkspace

#Get list of rasters
rlist = arcpy.ListRasters()

#print list of rasters

for raster in rlist:
	desc = arcpy.Describe(raster)
	crs = desc.SpatialReference
	print "{0} had CRS {1}".format(desc.basename,crs.name)
	print desc.basename[0:12] + " has a CRS of " + crs.name
	tempraster = outgdb_workspace + "/temp"  
	finalraster = outgdb_workspace + "/" +  desc.basename[0:12]
	print finalraster
	arcpy.ProjectRaster_management (raster, tempraster, sr, "CUBIC")
	arcpy.Clip_management(tempraster, "#", finalraster, extent, "#", "ClippingGeometry")
	arcpy.Delete_management(tempraster)
	
arcpy.env.workspace = outgdb_workspace
rlist = arcpy.ListRasters()
mosaic = ""
for raster in rlist:
	desc = arcpy.Describe(raster)
	crs = desc.SpatialReference
	print desc.basename[0:2]
	if desc.basename[0:2] == "m_":
		mosaic = desc.basename + ";" + mosaic
		print mosaic
		
arcpy.MosaicToNewRaster_management (mosaic, outgdb_workspace, "NAIP_2014", "#", "#", "#", 4)

#Working on attributes

#Inspect attributes for Black Hills and create label field to use for final map

import arcpy
arcpy.env.overwriteOutput = True

gdbworkspace = r'T:\users\Ekach\Final_Project\workspace.gdb'
extent = r'T:\users\Ekach\Final_Project\area_of_interest\workspace.gdb\area_of_interest'
sr = arcpy.SpatialReference(26913)

#Create hillshade from elevation raster and export to folder as a .tif

import arcpy
import arcpy.sa
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")
arcpy.env.overwriteOutput = True

ourasterbands =   r'T:\users\Ekach\Final_Project\published/'
arcpy.env.workspace= r'T:\users\Ekach\Final_Project\workspace.gdb'

#convert img to elevation raster in feet and export to hillshade
elev = arcpy.ListRasters("img*")
for raster in elev:
    #rasterObject = arcpy.Describe(raster)
	#name = rasterObject.basename 
	elevFeet = ourasterbands + "elevation_feet.tif"
	hillshade = ourasterbands + "elevation_hillshade.tif"
	r1 = arcpy.sa.Raster(raster)
	r2 = r1 * 3.281
	r2.save(elevFeet)
	arcpy.HillShade_3d(elevFeet, hillshade, 270, 55)
	
print "end"
arcpy.CheckInExtension("Spatial")
arcpy.CheckInExtension("30")

print (arcpy.GetMessages())

#output feature classes to published folder
arcpy.env.workspace = r'T:\users\Ekach\Final_Project\workspace.gdb'
outfc =  r'T:\users\Ekach\Final_Project\published/'

fclist = arcpy.ListFeatureClasses()

print fclist

for fc in fclist:
	#print fclist
	desc = arcpy.Describe(fc)
	arcpy.FeatureClassToFeatureClass_conversion(fc, outfc, desc.basename+ ".shp")
	
in_raster =  r'T:\users\Ekach\Final_Project\workspace.gdb\NAIP_2014'
out_rasterdataset = outfc + "NAIP2014.tif"
arcpy.CopyRaster_management(in_raster, out_rasterdataset)
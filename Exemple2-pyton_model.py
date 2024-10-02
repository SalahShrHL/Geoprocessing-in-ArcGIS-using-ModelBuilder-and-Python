#Créeation d’un ModelBuilder qui fait l’extraction d’un modèle hydrographique à partir d’une image raster en utilisant le langage python.
#un ensemble de modules Python permettant d'interagir avec les outils de géotraitement de ArcGIS.
import arcpy

# Les données en entrée (image raster + shape file)

rasterMila = "x1424454765.tif"
ouad_el_ethmania = "ouad_el_ethmania"

# Les fichiers où les différents résultats des opérations vont être stockés 

resultat1 = "C:\\Users\\SALAH PC\\Documents\\ArcGIS\\Default.gdb\\resultat1"
resultat2_1 = "C:\\Users\\SALAH PC\\Documents\\ArcGIS\\Default.gdb\\resultat2"
resultat2_2 = ""
resultat3 = "C:\\Users\\SALAH PC\\Documents\\ArcGIS\\Default.gdb\\resultat3"
resultat4 = "C:\\Users\\SALAH PC\\Documents\\ArcGIS\\Default.gdb\\resultat4"
resultat5 = "C:\\Users\\SALAH PC\\Documents\\ArcGIS\\Default.gdb\\resultat5"
resultat6 = "C:\\Users\\SALAH PC\\Documents\\ArcGIS\\Default.gdb\\resultat6"
resultat_final = "C:\\Users\\SALAH PC\\Documents\\ArcGIS\\Default.gdb\\resultat_final"




#######################################################################################################################################

##############     Découper la zone d’étude(ouad el ethmania) à partir du raster   ####################################################

arcpy.Clip_management(rasterMila, "6,3 36,2 6,4 36,4", resultat1, ouad_el_ethmania, "32767", "ClippingGeometry", "NO_MAINTAIN_EXTENT")



########################################################################################################################################

##############      Remplir les espaces vides  dans le raster en entrée
# (les pixel qui ne contient pas de valeurs):

arcpy.gp.Fill_sa(resultat1, resultat2_1, "")



########################################################################################################################################

##############   determiner la direction de flux , la direction de flux =la direction de l'écoulement d'eau dans une zone 

arcpy.gp.FlowDirection_sa(resultat2_1, resultat3, "NORMAL", resultat2_2, "D8")



########################################################################################################################################

############## 	creer un raster de flux accumulé dans chaque cellule

arcpy.gp.FlowAccumulation_sa(resultat3, resultat4, "", "FLOAT", "D8")



########################################################################################################################################

############## négliger les reseaux de petie taille

arcpy.gp.Con_sa(resultat4, resultat3, resultat5, "", "value>1000")



########################################################################################################################################

############## 	création des niveaux ou l’ordre de reseau hydrographique

arcpy.gp.StreamOrder_sa(resultat5, resultat3, resultat6, "STRAHLER")



########################################################################################################################################
#	Convertir la couche raster "resultat6" en une couche de polylignes "resultat_final"

tempEnvironment0 = arcpy.env.outputZFlag
arcpy.env.outputZFlag = "Disabled"
tempEnvironment1 = arcpy.env.outputMFlag
arcpy.env.outputMFlag = "Disabled"
arcpy.RasterToPolyline_conversion(resultat6, resultat_final, "ZERO", "0", "SIMPLIFY", "Value")
arcpy.env.outputZFlag = tempEnvironment0
arcpy.env.outputMFlag = tempEnvironment1


import rasterio
import matplotlib.pyplot as plt

filepath = '/home/anderson/gridfiles/DEM.tif'

source = rasterio.open(filepath)

print(source.crs) #CRS
print(source.res) #resolução
print(source.xy(10,20)) #coordenadas da céclula (linha, coluna)
print(source.lnglat()) 

raster = source.read(1)

plt.imshow(raster)
plt.show()


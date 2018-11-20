#### Create Leaflet Map for ski club 

library(leaflet)

# add a data table with trail data




skimap <- leaflet() %>%
  addTiles() %>%
  #addProviderTiles("OpenStreetMap.BlackAndWhite") %>%
  #addProviderTiles("Stamen.TerrainBackground")
  #names(providers)
  setView(lng = -127.229, lat = 54.735,zoom = 13)
 

skimap <- skimap %>% 
   addMarkers(lng = -127.219, lat = 54.735)

# install ggmap and import libraries
# install.packages('ggmap')
library(ggmap)
library(tidyverse)

# import datasets
crime <- read_csv('Crime_Data.csv')

# create address column
crime$address <- paste(crime$BlockNumber, ' ', crime$StreetName, ', Charlottesville, VA', sep='' )

# convert street address to geospacial data
for(i in 1:nrow(crime))
{
  result <- geocode(crime$address[i], output = "latlona", source = "dsk")
  crime$X[i] <- as.numeric(result[1])
  crime$Y[i] <- as.numeric(result[2])
}

# plot crime data
plot(crime$X, crime$Y)

# count unique addresses
length(unique(crime$address))
# 2177


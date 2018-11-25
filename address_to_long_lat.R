# install ggmap and import libraries
# install.packages('ggmap')
library(ggmap)
library(tidyverse)
library(plyr)

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

# create function to et most frequent value
getmode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

# find most frequent address
getmode(crime$address)
# 600 E MARKET ST, Charlottesville, VA - cville police department

# count number of times the address appears
sum(crime$address == '600 E MARKET ST, Charlottesville, VA')
# 1148

# frequency table of addresses
most_freq <- as.data.frame(count(crime$address))
most_freq <- most_freq[order(most_freq$freq, decreasing = TRUE),]

# ten most frequent addresses for crime
most_freq[1:10,]

#                                           x freq
# 1526   600 E MARKET ST, Charlottesville, VA 1148
# 1685  700 PROSPECT AVE, Charlottesville, VA  489
# 371     1100 5TH ST SW, Charlottesville, VA  351
# 1749      800 HARDY DR, Charlottesville, VA  327
# 1317    400 GARRETT ST, Charlottesville, VA  319
# 390    1100 EMMET ST N, Charlottesville, VA  314
# 615  1400 MELBOURNE RD, Charlottesville, VA  304
# 1801     800 W MAIN ST, Charlottesville, VA  264
# 605    1400 HAMPTON ST, Charlottesville, VA  248
# 1456       500 PARK ST, Charlottesville, VA  239

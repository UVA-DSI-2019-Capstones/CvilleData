# Import libraries
library(rvest)
library(tidyverse)
library(jsonlite)
library(data.table)
library(stringr)

# Function to iterate through all values of dataframe
lltoblock = function(df) {
  
  webpagelist = c()
  
  for(i in 1:nrow(df)) {
    
    # Get lat and long
    lat = df$Y[i]
    long = df$X[i]
    
    # Paste it into url
    url = paste('https://geo.fcc.gov/api/census/block/find?latitude=',
                lat,'&longitude=',long,'&showall=false&format=json', 
                sep="")

    webpage = read_html(url)
    
    webpagelist[i] = toString(webpage)
  }
  
  return(webpagelist)
}

# save output and extract block number
stored = lltoblock(as.data.frame(both))

# copy both and append block number to both
both_block <- both
both_block$Block <- sub(".*FIPS\\\":\\\" *(.*?) *\\\",\\\"bbox.*", "\\1", stored)



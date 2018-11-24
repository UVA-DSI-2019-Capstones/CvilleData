# Import libraries
library(tidyverse)
library(ggplot2)

# Read in data
bikerack = read_csv("data/bicycle_rack_points.csv")
busstop = read_csv("data/cat_bus_stop_points.csv")
firedept = read_csv("data/charlottesville_fire_department_station_locations.csv")
parkmeter = read_csv("data/parking_meter_pilot_locations_.csv")
names(parkmeter) = toupper(names(parkmeter))
votepoint = read_csv("data/voting_place_points.csv")

# Add variable to each indicating which dataframe it's from
bikerack$Source = 'BikeRack'
busstop$Source = 'BusStop'
firedept$Source = 'FireDept'
parkmeter$Source = 'ParkMeter'
votepoint$Source = 'VotePoint'

# Combine on X and Y with variable for BusStop or BikeRack
both = rbind(bikerack[, c('X', 'Y', 'Source')], busstop[, c('X', 'Y', 'Source')],
             firedept[, c('X', 'Y', 'Source')], parkmeter[, c('X', 'Y', 'Source')],
             votepoint[, c('X', 'Y', 'Source')])

# Plot all locations
ggplot(both, aes(x = X, y = Y)) + 
  geom_point(aes(color = Source, size = Source)) +
  scale_size_manual(values=c(1,1,3,1,3))



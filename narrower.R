
# Read in data
cville = read.csv("cville_conf.csv", header = FALSE, stringsAsFactors = FALSE)


narrow = data.frame(matrix(ncol = 4, nrow = 30000))
names(narrow) = c("dataset", "variable", "description", "confidence")


# Initialize an indexing count for narrow data frame
count = 1
# Loop through cville rows
for(i in 3:dim(cville)[1]) {
  
# Loops through cville columns
  for(j in 2:dim(cville)[2]) {
    
#If value is not NA, then add to our data frame
    if(!is.na(cville[i,j])) {
      
      
      narrow$dataset[count] = cville[i,1]
      narrow$variable[count] = cville[1,j]
      narrow$description[count] = cville[2,j]
      narrow$confidence[count] = as.numeric(cville[i,j])
      count = count + 1
    }
  }
}

narrow = as.data.frame(narrow[complete.cases(narrow$confidence),])

write.csv(x = narrow, file = "narrow.csv")


as.numeric(cville[5,2])


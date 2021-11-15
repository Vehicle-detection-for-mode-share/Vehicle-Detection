# list all txt files in path
list_of_files <- list.files(path = "C:/Users/Kyriaki Kokka/Desktop/Cities_csv/HongKong", recursive = TRUE,
                            pattern = "\\.txt$", 
                            full.names = TRUE)

# IMPORTANT: delete JSON.zip.txt

# Read all the files and create a FileName column to store filenames
library(data.table)
DT <- rbindlist(sapply(list_of_files, fread, simplify = FALSE),
                use.names = TRUE, idcol = "FileName")

# write to csv
write.csv(DT, 'C:/Users/Kyriaki Kokka/Desktop/Cities_csv/HongKong.csv', row.names=FALSE)

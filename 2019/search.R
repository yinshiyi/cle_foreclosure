setwd("C:/Users/Shiyi/OneDrive/python")
quary=as.data.frame(read.csv("LotSearchresults_2019 August 15 (1).csv"))
database=as.data.frame(read.csv("copart20190816-095335.csv"))
for (r in c(1:nrow(quary))) {
  quary$finalprice[r]=as.integer(database[which(database$lotnum%in%(quary$Lot..[r])),3])[1]
  #print(as.integer(database[which(database$lotnum%in%(quary$Lot..[r])),]))
  }
interest=merge(quary,database,by.x="Lot..",by.y="lotnum")[7,]

write.csv(interest,"shiyilist.csv",append=T)

#merge the two list by row and save one ultimate list and fill in the blank of the sold price on autostat
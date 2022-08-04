library("ggplot2")
library("ggrepel")
setwd("C:/Users/Shiyi/OneDrive/python")
a <- data.frame(stringsAsFactors=FALSE,
           index = c(4, 16, 26, 5, 23),
         Address = c("3227 WEST 114TH STREET cuyahoga county, OH",
                     "12524 PARK KNOLL DRIVE cuyahoga county, OH",
                     "987 CHELSTON ROAD cuyahoga county, OH",
                     "3544 WEST 127TH STREET cuyahoga county, OH", "756 RADFORD DRIVE cuyahoga county, OH"),
          status = c("ACTIVE", "ACTIVE", "ACTIVE", "ACTIVE", "ACTIVE"),
           price = c(23334, 26667, 33334, 40000, 40000),
   orignialprice = c(35000, 40000, 50000, 60000, 60000),
             gps = c("3227, West 114th Street, Little Arabia, Cudell,
                     Cleveland, Cuyahoga County, Ohio, 44111, USA", "12524,
                     Park Knoll Drive, Garfield Heights, Cuyahoga County, Ohio,
                     44125, USA", "987, Chelston Road, South Euclid, Cuyahoga County,
                     Ohio, 44121, USA", "3544, West 127th Street, Jefferson,
                     Cleveland, Cuyahoga County, Ohio, 44111, USA", "756,
                     Radford Drive, Highland Heights, Cuyahoga County, Ohio, 44143, USA"),
        latitude = c(41.46445, 41.42532, 41.53333, 41.4561, 41.54176),
       longitude = c(-81.7656, -81.5956, -81.526, -81.7768, -81.4886),
         zipcode = c(44111, 44125, 44121, 44111, 44143),
            safe = c(FALSE, FALSE, FALSE, FALSE, FALSE)
)
a <- read.csv("nextdate.csv")
b <-lapply(a$Address, gsub, pattern = " cuyahoga county, OH", replacement = "", fixed = TRUE)
a$Addressshort=paste(b,'\n',as.character(a$price),as.character(a$white),as.character(a$asian),as.character(a$income))
a[which(a$Address=="2476 Derbyshire Rd"),'Addressshort']=c("2476 Derbyshire Rd \n listed, white, asian, income")
plot <-
  ggplot(a, aes(x = longitude, y = latitude) ) + geom_point(size = 2) +
  geom_text_repel(aes(label = Addressshort), size = 4,force = 10) +
  coord_fixed(
    ratio = 1,
    xlim = NULL,
    ylim = NULL,
    expand = TRUE,
    clip = "on"
  ) + theme_bw() +
  #geom_point(aes(x = -81.591807, y = 41.502176), colour = "blue")+
  #geom_text(x=-81.601807, y=41.502176, label="HQ")+
  ggtitle(paste("Plot of upcoming autction",as.character(Sys.Date())))


ggsave(plot, filename = gsub(":","-",paste(as.character(Sys.time()),"rplot.pdf")),device = "pdf")

#install package rcopanion so you can plot histogram and do VAR modeling

install.packages("rcompanion")
install.packages("ggplot2")
install.packages("vars") #for VAR modeling
install.packages("astsa") #for VAR modeling

library(rcompanion)
library(ggplot2)
library(vars)
library(astsa)

#set working path and load in data
outintech<- read.csv(file="~/Desktop/FAANG3.csv")

#specifying reference levels for Company
Company.rel<- relevel(outintech$Company, ref="Amazon")

# check variable data types
str(outintech)

#creating a vector of response variables
x = cbind( outintech$Revenue, outintech$SGA, outintech$NetIncome,
           outintech$FreeCashFlow, outintech$GrossProfit, outintech$StockPrice)
#plotting and creating var autoregressive model
plot.ts(x , main = "", xlab = "")
fitvar1=VAR(x, p=1, type='const')
summary(fitvar1)

#including less metrics into VAR by combining some metrics
x = cbind( outintech$NetIncMargin, outintech$GrossProfMargin, outintech$SGA,
           outintech$FreeCashFlow, outintech$StockPrice)

plot(outintech$NetIncMargin, main="Net Income Margin", xlab="")
plot.ts(x , main = "", xlab = "")
fitvar1=VAR(x, p=1, type='const')
summary(fitvar1)



# Scatter plot of outcome (StockPrice) against Revenue
qplot( Revenue, StockPrice, data = outintech, size=NetIncome, color=Year )
#checking correlation between Stock Price and Revenue
with(outintech, cor(Revenue, StockPrice))
#correlation is positive which makes sense

# Scatter plot of outcome (StockPrice) against NetIncome
qplot (NetIncome, StockPrice, data = outintech, color=Year )
#checking correlation between Stock Price and Net Income
with(outintech, cor(NetIncome, StockPrice))
#correlation between StockPrice and Net Income is negative 

#checking correlation of StockPrice with GrossProfMargin
qplot (GrossProfMargin, StockPrice, data = outintech )
with(outintech, cor(GrossProfMargin, StockPrice))

#Boxplots showing StockPrice broken down by Company
qplot (Company, StockPrice, geom = "boxplot", data = outintech)

#do simple regression
summary(fittedoutintech<- lm(outintech$StockPrice 
                             ~ outintech$Year
                             + Company.rel
                             + outintech$Revenue
                             + outintech$NetIncome
                             + outintech$FreeCashFlow
                             + outintech$GrossProfit
                             + outintech$SGA
                             , data = outintech
                             ))

#simple regression for combined metrics
summary(fittedoutintech<- lm(outintech$StockPrice 
                             ~ outintech$Year
                             + outintech$Company
                             + outintech$Revenue
                             + outintech$NetIncome
                             + outintech$NetIncPer
                             + outintech$FreeCashFlow
                             + outintech$GrossProfit
                             + outintech$SGA
                             , data = outintech
))

summary(fittedoutintech<- lm(outintech$StockPrice 
                             ~ outintech$Year
                             + Company.rel
                             + outintech$NetIncPer
                             + outintech$FreeCashFlow
                             + outintech$GrossProfit
                             + outintech$SGA
                             , data = outintech
))

# Correlation of Stock with NetIncMargin
qplot( NetIncPer, StockPrice, data = outintech, color=Company.rel, size = Year )
with(outintech, cor(NetIncPer, StockPrice))
#correlation=-0.3867938 is negative and quite big, NetIncome/Revenue can be used as a key ratio  

#checking correlation of StockPrice with GrossProfMargin
qplot (GrossProfMargin, StockPrice, data = outintech )
with(outintech, cor(GrossProfMargin, StockPrice))
#correlation is -0.3135. GrossProfitMargin can be used as a key ratio.

qplot (GrossProfMargin, StockPrice, data = outintech )
with(outintech, cor(GrossProfMargin, StockPrice))

#correlation of StockPrice with SGA is 0.619
qplot (SGA, StockPrice, data = outintech )
with(outintech, cor(SGA, StockPrice))

#correlation of StockPrice with FreeCashFlow is -0.10578
qplot (FreeCashFlow, StockPrice, data = outintech )
with(outintech, cor(FreeCashFlow, StockPrice))

#correlation of StockPrice with GrossProfit is 0.24496
qplot (GrossProfit, StockPrice, data = outintech )
with(outintech, cor(GrossProfit, StockPrice))

#correlation matrix
head(outintech, 5)
res <- cor(outintech)
round(res, 2)


#plot data
plot(fittedoutintech)

plotNormalHistogram(residuals(fittedoutintech))






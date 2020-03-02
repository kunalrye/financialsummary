# Code for gathering the first CIKS, for the companies in the S&P 500 IT sector (fund) 


#ticker_to_cik from http://rankandfiled.com/#/data/tickers
#tech_stock_tickers from https://www.barchart.com/stocks/indices/sp-sector/information-technology?viewName=main

#Open the files with the tickers and company names
ciks = read.csv("ticker_to_cik.csv")
cos = read.csv("all_technology_stocks.csv")
#create empty lists for tickers, ciks and company names
ticker = c()
cik= c()
company =c()

#loop over all tickers and see if they are a tech stock, then add to lists
for(idx in 1:length(ciks$Ticker)){
  if(ciks$Ticker[idx] %in% cos$Ticker){
    ticker = c(ticker, toString(ciks$Ticker[idx]))
    cik= c(cik, ciks$CIK[idx])
    company = c(company, toString(ciks$Name[idx]))
  }
}
# Create the dataframe of companies
data= data.frame(
  "CompanyName" = company, 
  "CIK" = cik,
  "Ticker" = ticker)
#save the df as a csv
write.csv(data,'all_TechStocks_NameCIKTicker.csv',row.names=FALSE)


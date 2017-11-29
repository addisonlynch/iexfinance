from .iexretriever import IEXRetriever, IEXSymbolError, IEXEndpointError, IEXDatapointError
from .iexretriever import IEXQueryError
__author__ = 'Addison Lynch'
__version__ = '0.2'
__all__ = ['Share', 'Batch']



def IexFinance(symbol, **kwargs):
	if type(symbol) is str:
		if not symbol:
			raise ValueError("Please input a symbol or list of symbols")
		else:
			inst = Share(symbol, **kwargs)
	elif type(symbol) is list:
		if not symbol:
			raise ValueError("Please input a symbol or list of symbols")
		if len(symbol) == 1:
			inst = Share(symbol, **kwargs)
		if len(symbol) > 50:
			raise ValueError("Invalid symbol list. Maximum 50 symbols.")
		else:
			inst = Batch(symbol, **kwargs)
		return inst
	else:
		raise TypeError("Please input a symbol or list of symbols")
	return inst
		
class Share(IEXRetriever):

    key="Share"

    def __init__(self,symbol, **kwargs):

        self.symbol = symbol.upper()
        self.symbolList = [self.symbol]
        self.IEX_ENDPOINT_NAME = 'stock/{0}/batch'.format(self.symbol)
        super(Share, self).__init__(self.key, self.symbolList, **kwargs)
        self.data_set = self.refresh()        


    def refresh(self):
        data = super(Share, self)._fetch()
        self.data_set = data[self.symbol]
        return data[self.symbol]
    # universal selectors
    def get_select_endpoints(self, endpointList=[]):
        if type(endpointList) is str:
            endpointList = [endpointList]
        result = {}
        if not endpointList:
            raise ValueError("Please provide a valid list of endpoints")
        for endpoint in endpointList:
            try:
                query = self.data_set[endpoint]
            except:
                raise IEXEndpointError(endpoint)
            result.update({endpoint: query})
        return result

    def get_select_datapoints(self, endpoint, attrList= []):
        if type(attrList) is str:
            attrList = [attrList]
        result = {}
        if not attrList:
            raise ValueError("Please give a valid attribute list")
        try:
            ep = self.data_set[endpoint]
        except:
            raise IEXEndpointError(endpoint)
        for attr in attrList:
            try:
                query = ep[attr]
            except:
                raise IEXDatapointError(endpoint, attr)
            result.update({attr: query})
        return result

    # endpoint methods

    def get_quote(self):
        return self.data_set["quote"]
    def get_chart(self):
        return self.data_set["chart"]
    def get_book(self):
        return self.data_set["book"]
    def get_open_close(self):
        return self.data_set["open-close"] # fix
    def get_previous(self):
        return self.data_set["previous"]
    def get_company(self):
        return self.data_set["company"]
    def get_key_stats(self):
        return self.data_set["stats"] # fix
    def get_peers(self):
        return self.data_set["peers"]
    def get_relevant(self):
        return self.data_set["relevant"]
    def get_news(self):
        return self.data_set["news"]
    def get_financials(self):
        return self.data_set["financials"]
    def get_earnings(self):
        return self.data_set["earnings"]
    def get_logo(self):
        return self.data_set["logo"]
    def get_price(self):
        return self.data_set["price"]
    def get_delayed_quote(self):
        return self.data_set["delayed-quote"] # fix
    def get_effective_spread(self):
        return self.data_set["effective-spread"] # fix
    def get_volume_by_venue(self):
        return self.data_set["volume-by-venue"] # fix
    def get_all(self):
        return self.data_set
    def get_yesterdays_close(self):
        return self.data_set["previousClose"]
    def get_dividends(self):
        return self.data_set["dividends"]
    def get_splits(self):
        return self.data_set["splits"]



    #datapoint methods
    def get_company_name(self):
        return self.get_quote()["companyName"]
    def get_primary_exchange(self):
        return self.get_quote()["primaryExchange"]
    def get_sector(self):
        return self.get_quote()["sector"]
    def get_symbol(self):
        return self.get_quote()["symbol"]
    def get_open(self):
        return self.get_quote()["open"]
    def get_close(self):
        return self.get_quote()["close"]
    def get_years_high(self):
        return self.get_quote()["week52High"]
    def get_years_low(self):
        return self.get_quote()["week52Low"]
    def get_ytd_change(self):
        return self.get_quote()["ytdChange"]
    def get_volume(self):
        return self.get_quote()["latestVolume"]
    def get_market_cap(self):
        return self.get_quote()["marketCap"]
    def get_beta(self):
        return self.get_key_stats()["beta"]
    def get_short_interest(self):
        return self.get_key_stats()["shortInterest"]
    def get_short_ratio(self):
        return self.get_key_stats()["shortRatio"]
    def get_latest_eps(self):
        return self.get_key_stats()["latestEPS"]
    def get_shares_outstanding(self):
        return self.get_key_stats()["sharesOutstanding"]
    def get_float(self):
        return self.get_key_stats()["float"]
    def get_eps_consensus(self):
        return self.get_key_stats()["consensusEPS"]
    def get_primary_exchange(self):
        return self.get_quote()["primaryExchange"]


class Batch(IEXRetriever):

    IEX_ENDPOINT_NAME = 'stock/market/batch'
    key = 'Batch'
    
    def __init__(self,symbolList=[], **kwargs):

        super(Batch, self).__init__(self.key, symbolList, **kwargs)
        
        self.data_set = self.refresh()
    
    def refresh(self):
        data = super(Batch, self)._fetch()
        diff = set(self.symbolList) - set(data.keys())
        if diff:
            raise IEXSymbolError(diff[0])
        else:
            return data

    #universal selectors
    def get_select_endpoints(self, endpoints=[]):
        
            if type(endpoints) is str:
                endpoints = [endpoints]
            elif not endpoints:
                raise ValueError("Please provide a valid list of endpoints")
            result = {}
            for symbol in self.symbolList:
                temp = {}
                try:
                    ds = self.data_set[symbol]
                except:
                    IEXSymbolError(symbol)
                for endpoint in endpoints:
                    try:
                        query = ds[endpoint]
                    except:
                        raise IEXEndpointError(endpoint)
                    temp.update({endpoint: query})
                result.update({symbol:temp})
            return result

    def get_select_datapoints(self, endpoint, attrList= []):
        if type(attrList) is str:
            attrList = [attrList]
        result = {}
        if not attrList:
            raise ValueError("Please give a valid attribute list")
        for symbol in self.symbolList:
            try: 
                ep = self.data_set[symbol][endpoint]
            except:
                raise IEXEndpointError(endpoint)
            temp = {}
            for attr in attrList:
                try:
                    query = ep[attr]
                except:
                    raise IEXDatapointError(endpoint, attr)
                temp.update({attr: query})
            result.update({symbol:temp})
        return result

    @IEXRetriever._output_format
    def get_all(self):
        return self.data_set

    #endpoint methods
    @IEXRetriever._output_format
    def get_quote(self):
        return {symbol: self.data_set[symbol]["quote"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_book(self):
        return {symbol: self.data_set[symbol]["book"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_chart(self):
        return {symbol: self.data_set[symbol]["chart"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_open_close(self):
        return {symbol: self.data_set[symbol]["open-close"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_previous(self):
        return {symbol: self.data_set[symbol]["previous"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_company(self):
        return {symbol: self.data_set[symbol]["company"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_key_stats(self):
        return {symbol: self.data_set[symbol]["stats"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_peers(self):
        return {symbol: self.data_set[symbol]["peers"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_relevant(self):
        return {symbol: self.data_set[symbol]["relevant"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_news(self):
        return {symbol: self.data_set[symbol]["news"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_financials(self):
        return {symbol: self.data_set[symbol]["financials"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_earnings(self):
        return {symbol: self.data_set[symbol]["earnings"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_dividends(self):
        return {symbol: self.data_set[symbol]["dividends"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_splits(self):
        return {symbol: self.data_set[symbol]["splits"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_logo(self):
        return {symbol: self.data_set[symbol]["logo"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_price(self):
        return {symbol: self.data_set[symbol]["price"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_delayed_quote(self):
        return {symbol: self.data_set[symbol]["delayed-quote"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_effective_spread(self):
        return {symbol: self.data_set[symbol]["effective-spread"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_volume_by_venue(self):
        return {symbol: self.data_set[symbol]["volume-by-venue"] for symbol in self.data_set.keys()}

    # datapoint methods
    @IEXRetriever._output_format
    def get_company_name(self):
        return {symbol: self.get_quote()[symbol]["companyName"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_primary_exchange(self):
        return {symbol: self.get_quote()[symbol]["primaryExchange"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_sector(self):
        return {symbol: self.get_quote()[symbol]["sector"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_open(self):
        return {symbol: self.get_quote()[symbol]["open"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_close(self):
        return {symbol: self.get_quote()[symbol]["close"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_years_high(self):
        return {symbol: self.get_quote()[symbol]["week52High"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_years_low(self):
        return {symbol: self.get_quote()[symbol]["week52Low"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_ytd_change(self):
        return {symbol: self.get_quote()[symbol]["ytdChange"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_volume(self):
        return {symbol: self.get_quote()[symbol]["latestVolume"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_market_cap(self):
        return {symbol: self.get_quote()[symbol]["marketCap"]for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_beta(self):
        return {symbol: self.get_key_stats()[symbol]["beta"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_short_interest(self):
        return {symbol: self.get_key_stats()[symbol]["shortInterest"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_short_ratio(self):
        return {symbol: self.get_key_stats()[symbol]["shortRatio"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_latest_eps(self):
        return {symbol: self.get_key_stats()[symbol]["latestEPS"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_shares_outstanding(self):
        return {symbol: self.get_key_stats()[symbol]["sharesOutstanding"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_float(self):
        return {symbol: self.get_key_stats()[symbol]["float"] for symbol in self.data_set.keys()}
    @IEXRetriever._output_format
    def get_eps_consensus (self):
        return {symbol: self.get_key_stats()[symbol]["consensusEPS"] for symbol in self.data_set.keys()}

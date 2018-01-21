import sys
import os

import unittest
import mock

import simplejson as json

from iexfinance import Share, Batch 
from iexfinance import IexFinance as iex
from iexfinance.utils.symbols import get_available_symbols#, IEXSymbolError, IEXDatapointError, IEXEndpointError, IEXQueryError


class mocker(object):

	@classmethod
	def get_sample_share_data(cls):
		with open("tests/sample_data_share.json") as json_data:
			x = json.load(json_data)
			if not x:
				raise ValueError("sample_data_share.json is not properly formatted or is empty")
			return x

	@classmethod
	def get_sample_batch_data(cls):
		with open("tests/sample_data_batch.json") as json_data:
			x = json.load(json_data)
			if not x:
				raise ValueError("sample_data_batch.json is not properly formatted or is empty")
			return x

	@classmethod
	@mock.patch.object(Share, 'refresh')
	def get_mock_share(cls, mock_method):
		mock_method.return_value = cls.get_sample_share_data()
		inst = Share("luv")
		return inst

	@classmethod
	@mock.patch.object(Batch, 'refresh')
	def get_mock_batch(cls, mock_method):
		mock_method.return_value = cls.get_sample_batch_data()
		inst = Batch(["lol"])
		return inst

class BaseTester(unittest.TestCase):

	def test_wrong_iex_input_type(self):
		with self.assertRaises(TypeError):
			iex(34)
		with self.assertRaises(ValueError):
			iex("")
		with self.assertRaises(ValueError):
			l = []
			iex(l)

	def test_symbol_list_too_long(self):
		with self.assertRaises(ValueError):
			x = ["tsla"] * 102
			iex(x)	

	def test_wrong_option_values(self):
		with self.assertRaises(ValueError):
			iex("aapl", last=555)

		with self.assertRaises(TypeError):
			iex("aapl", displayPercent=4)

		with self.assertRaises(ValueError):
			iex("aapl", dividendsRange='6y')

		with self.assertRaises(ValueError):
			iex("aapl", splitsRange='9a')

		with self.assertRaises(ValueError):
			iex("aapl", chartRange='1yy')

	# def test_invalid_option_values(self):
	# 	with self.assertRaises(TypeError):
	# 		iex("aapl", displayPercent=4)
	# 	with self.assertRaises(ValueError):
	# 		iex("aapl", last=68)
	# 	with self.assertRaises(ValueError):
	# 		iex("aapl", chartRange='6y')
	# 	with self.assertRaises(ValueError):
	# 		iex("aapl", )


class ShareIntegrityTester(unittest.TestCase):

	def setUp(self):
		self.mshare = mocker.get_mock_share()
		self.cshare = Share(self.mshare.get_symbol())

	def test_endpoints(self):
		mendpoints = list(self.mshare.get_all().keys())
		cendpoints = list(self.cshare.get_all().keys())
		mendpoints.sort()
		cendpoints.sort()
		self.assertListEqual(mendpoints, cendpoints)



	def test_datapoints(self):
		table = self.mshare.get_all()
		for endpoint in table.keys():
			mmod = self.mshare.get_select_endpoints(endpoint)
			cmod = self.cshare.get_select_endpoints(endpoint)
			self.assertEqual(type(mmod), type(cmod))
			if type(mmod) is dict:
				print("testing endpoint: " + endpoint +"...", end=" ")
				mdatapoints = list(mmod.keys())
				cdatapoints = list(cmod.keys())
				mdatapoints.sort()
				cdatapoints.sort()
				self.assertListEqual(mdatapoints, cdatapoints)
				print("...PASSED")
			else:
				print("Skipping endpoint " + endpoint)
		self.assertListEqual(mdatapoints, cdatapoints)



class BatchIntegrityTester(unittest.TestCase):

	def setUp(self):
		self.mbatch = mocker.get_mock_batch()
		self.cbatch = Batch(["aapl", "tsla"])
		self.mshares = []
		
	#def test_symbols(self):
		#print("ran test_symbols!")
		#self.assertListEqual(list(self.mbatch.get_all().keys()).sort(), list(self.cbatch.get_all().keys()).sort())



class Sharetester(unittest.TestCase):

	def setUp(self):
		self.cshare = Share("aapl")


	def test_get_all_format(self):
		data = self.cshare.get_all()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_chart_format(self):
		data = self.cshare.get_chart()
		self.assertIsInstance(data, list, "Result expected list")

	def test_get_book_format(self):
		data = self.cshare.get_book()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_open_close_format(self):
		data = self.cshare.get_open_close()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_previous_format(self):
		data = self.cshare.get_previous()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_company_format(self):
		data = self.cshare.get_company()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_key_stats_format(self):
		data = self.cshare.get_key_stats()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_relevant_format(self):
		data = self.cshare.get_relevant()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_news_format(self):
		data = self.cshare.get_news()
		self.assertIsInstance(data, list, "Result expected list")

	def test_get_financials_format(self):
		data = self.cshare.get_financials()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_earnings_format(self):
		data = self.cshare.get_earnings()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_logo_format(self):
		data = self.cshare.get_logo()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_price_format(self):
		data = self.cshare.get_price()
		self.assertIsInstance(data, float, "Result expected float")

	def test_get_delayed_quote_format(self):
		data = self.cshare.get_delayed_quote()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_effective_spread_format(self):
		data = self.cshare.get_effective_spread()
		self.assertIsInstance(data, list, "Result expected list")

	def test_get_volume_by_venue_format(self):
		data = self.cshare.get_volume_by_venue()
		self.assertIsInstance(data, list, "Result expected list")



class BatchTester(unittest.TestCase):

	def setUp(self):
		self.cbatch = Batch(["aapl", "tsla"])

		
	def test_invalid_symbol_or_symbols(self):
		with self.assertRaises(IEXSymbolError):
			iex(["TSLA", "AAAPLPL", "fwoeiwf"])

	def test_get_all_format(self):
		data = self.cbatch.get_all()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_chart_format(self):
		data = self.cbatch.get_chart()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_book_format(self):
		data = self.cbatch.get_book()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_open_close_format(self):
		data = self.cbatch.get_open_close()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_previous_format(self):
		data = self.cbatch.get_previous()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_company_format(self):
		data = self.cbatch.get_company()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_key_stats_format(self):
		data = self.cbatch.get_key_stats()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_relevant_format(self):
		data = self.cbatch.get_relevant()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_news_format(self):
		data = self.cbatch.get_news()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_financials_format(self):
		data = self.cbatch.get_financials()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_earnings_format(self):
		data = self.cbatch.get_earnings()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_logo_format(self):
		data = self.cbatch.get_logo()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_price_format(self):
		data = self.cbatch.get_price()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_delayed_quote_format(self):
		data = self.cbatch.get_delayed_quote()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_effective_spread_format(self):
		data = self.cbatch.get_effective_spread()
		self.assertIsInstance(data, dict, "Result expected dictionary")

	def test_get_volume_by_venue_format(self):
		data = self.cbatch.get_volume_by_venue()
		self.assertIsInstance(data, dict, "Result expected dictionary")


class UtilsTester(unittest.TestCase):

	def test_available_symbols(self):
		f = True
		if not get_available_symbols():
			f = False
		self.assertEqual(f, True)



if __name__=="__main__":
	unittest.main()

import numpy as np
from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Indicators")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from datetime import datetime

class RSIAlgo(QCAlgorithm):

    SYM = "AAPL"            # define symbol here
    RSI_BUY_DAILY = 50      # buy when RSI daily is greater than (bullish indicator)
    RSI_BUY_HOURLY = 20     # buy on pullback when RSI hour is less than 
    RSI_SELL_DAILY = 30     # liquidate when RSI daily is less than
    RSI_SELL_HOURLY = 50    # liquidate when RSI hour is greater than (bearish indicator)
    
    def Initialize(self):
        self.SetStartDate(2018, 1, 1)   # Set Start Date
        self.SetEndDate(2020, 1, 1)     # Set End Date
        self.SetCash(100000)            # Set Strategy Cash
        self.sym = self.AddEquity(self.SYM, Resolution.Minute)
        self.sym.SetDataNormalizationMode(DataNormalizationMode.Raw)
        
        # define a 14-period daily and hourly RSI indicators
        self.rsiD = self.RSI(self.SYM, 14, MovingAverageType.Simple, Resolution.Daily)
        self.rsiH = self.RSI(self.SYM, 14, MovingAverageType.Simple, Resolution.Hour)
        
        self.SetWarmUp(RSI_BUY_DAILY)


    def OnData(self, data):
        # check RSI status
        if self.rsiD.IsReady and self.rsiH.IsReady:
            
            if self.rsiD.Current.Value > self.RSI_BUY_DAILY and self.rsiH.Current.Value < self.RSI_BUY_HOURLY:
                if not self.Portfolio.Invested:
                    self.SetHoldings(self.SYM, 1)
            
            if self.rsiD.Current.Value < self.RSI_SELL_DAILY and self.rsiH.Current.Value > self.RSI_SELL_HOURLY:
                if self.Portfolio.Invested:
                    self.Liquidate(self.SYM)
    
    def OnEndOfDay(self):
        self.Plot("Indicators","RSI", self.rsiD.Current.Value)

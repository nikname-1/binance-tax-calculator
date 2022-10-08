# Binance Tax Calculation Tool

A simple way of calculating tax on staking/interest earnings from Binance. 

---
## General Use Case 
 - Two cases
    - Capital Gains (On interest/staking)
    - Income Tax (On interest/staking)
    - Capital Gains (Over time period for fiat) - TODO

 - Input a date range and calculate equivalent fiat earned (staking/interest earning, etc) for income tax.
 - Additional to the previous point, keep track of cost base of that earning for future calculation of capital gains. 
 - Calculate and store fiat inputs (buy/deposit prices) to CSV or read from existing CSV. - TODO
 - Use argParse or otherwise to allow user input through CLI



Important to follow Binance API limits! Do not run this too many times within a short period of time as you MAY exceed Binance's API limits. 

---

## User Guide

Run the calculator passing the following parameters. Currently works for AUD as the base currency by default. 

```
python binance_tax.py --start DD-MM-YYY --end DD-MM-YYYY --asset TICKER
```


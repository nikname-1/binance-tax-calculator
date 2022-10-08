import argparse
import api_functions_test as aft
parser = argparse.ArgumentParser(description="Process inputs for Binance Tax Tool")
parser.add_argument('--start', help="Date to start from.", required=True)
parser.add_argument('--end', help="End of interval date.", required=True)
parser.add_argument('--asset', help="Specify Symbol")

args = parser.parse_args()
startTimePOSIX = aft.convert_to_posix(args.start)
endTimePOSIX = aft.convert_to_posix(args.end)


total = aft.dividend_over_timeframe(startTime=startTimePOSIX, endTime=endTimePOSIX, asset = args.asset)
print(total)
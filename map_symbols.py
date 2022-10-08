
# Map symbols to AUD based on valid shortest path.
import json
import api_functions_test as aft
# i.e. for ALGO we want ALGOAUD -> which does not exist so we must map it via ALGOBNB -> BNBAUD or something similar
# Like searching through a graph to find shortest path between [LOCAL CURRENCY] and [CRYPTOCURRENCY]
def dump_exchange_info():
    with open('exchange_info.json','w') as file:
        json.dump(aft.exchange_info(), file)

def get_only_symbols():
    '''
    Extracts only symbol information (list) from 'exchange info' raw api dump 
    '''
    with open("exchange_info.json") as jsonFile:    
        exchange_info = json.load(jsonFile) 
        with open("symbols.json", 'w') as file:
            json.dump(exchange_info["symbols"], file)
        

def create_graph():
    '''
    Turn list of symbols into a one way? graph of symbols. 
    i.e. We want to convert a cryptocurrency to another currency how can we find the shortest path in this graph.
    '''
    SYMBOL_GRAPH = {} 
    PRIORITY_SYMBOL = 'AUD'
    def add_edge(base, quote, isReverse):
        # Base Currency is typically the asset being traded
        # Quote Currency is the asset in which trading is denominated. 
        # i.e. how much 1 Base Currency goes for.
        # Rate has to be calculated live.

        if base in SYMBOL_GRAPH:
            SYMBOL_GRAPH[base][quote]=isReverse
        else:
            SYMBOL_GRAPH[base] = {quote:isReverse}


    with open("symbols.json") as jsonFile:    
        symbols = json.load(jsonFile)
        for symbol in symbols:
            add_edge(symbol['baseAsset'], symbol['quoteAsset'], False)
            # print(symbol['baseAsset'], symbol['quoteAsset'])
            # add_edge(symbol['quoteAsset'], symbol['baseAsset'], True)
    

    with open('symbol_graph.json', 'w') as symbol_graph:
        json.dump(SYMBOL_GRAPH, symbol_graph)



# Run the following three functions to generate the symbol_graph.json file if required.
dump_exchange_info()
get_only_symbols()
create_graph()
from data import retrieve_data
import pandas as pd
import time

def create_frame(ticker_dictionary, annual=None, trailing=None):

    potential_annual = [
        'price_return', 'nav_return', 'benchmark_return', 'category_return', 'expense_ratio', 'turnover ratio', 'category_rank'
    ]
    potential_trailing = [
        'price_return', 'nav_return', 'benchmark_return', 'category_return', 'category_rank'
    ]

    index = [ticker for ticker in ticker_dictionary]
    annual_columns = []
    trailing_columns = []
    data = []
    if annual is not None:
        if annual == 'all':
            for label in potential_annual:
                annual_columns.append('a_' + label)
        else:
            assert(type(annual) == list), 'Enter trailing labels as a list.'
            for label in annual:
                assert (label in potential_annual), 'Invalid trailing label provided: ' + label 
                for tag in ticker_dictionary[index[0]]['annual'][label]:
                    annual_columns.append('a' + '_' + label + '_' + tag)
        subdata = {}
        for ticker in ticker_dictionary:
            temp_data = []
            for label in ticker_dictionary[ticker]['annual']:
                if label in annual:
                    for tag in ticker_dictionary[ticker]['annual'][label]:
                        temp_data.append(ticker_dictionary[ticker]['annual'][label][tag])
            try:
                subdata[ticker] = subdata[ticker] + temp_data
            except:
                subdata[ticker] = temp_data
        for key in subdata:
            data.append(subdata[key])

    if trailing is not None:
        if trailing == 'all':
            for label in potential_trailing:
                trailing_columns.append('t_' + label)
        else:
            assert(type(trailing) == list), 'Enter trailing labels as a list.'
            for label in trailing:
                assert (label in potential_trailing), 'Invalid trailing label provided: ' + label 
                for tag in ticker_dictionary[index[0]]['trailing'][label]:
                    trailing_columns.append('t' + '_' + label + '_' + tag)
        subdata = {}
        for ticker in ticker_dictionary:
            temp_data = []
            for label in ticker_dictionary[ticker]['trailing']:
                if label in trailing:
                    for tag in ticker_dictionary[ticker]['trailing'][label]:
                        temp_data.append(ticker_dictionary[ticker]['trailing'][label][tag])
            try:
                subdata[ticker] = subdata[ticker] + temp_data
            except:
                subdata[ticker] = temp_data
        for key in subdata:
            data.append(subdata[key])
    dataframe = pd.DataFrame(
        data=data, index=index, columns=annual_columns+trailing_columns
    )
    return dataframe
    
    
        

data = retrieve_data(['spy', 'bnd', 'vfiax'])
frame = create_frame(data, trailing = ['price_return', 'nav_return'], annual=['price_return'])

# fix 'columns passed' error, I think it has something to do with dictionary use

frame.to_csv('book1.csv')
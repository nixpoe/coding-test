class BackwardAdjusted:
    def __init__(self, data):
        self.data = data

    def backward_adj(self):
        df = self.data.copy()

        # sort by ticker and date(oldest -> newest)
        df = df.sort_values(['ticker_symbol', 'datetime'], ascending=[True, True])
        
        for ticker in df['ticker_symbol'].unique():
            mask = df['ticker_symbol'] == ticker
            sub = df.loc[mask].copy()  # Get data for just this ticker
            
            # Start from most recent (no adjustment needed)
            adjusted_prices = [0] * len(sub)
            adjusted_prices[-1] = sub.iloc[-1]['unadjusted_close']  # most recent price unchanged

            cumulative_factor = 1.0 
            
            # Work backwards from second-to-last
            for i in range(len(sub) - 2, -1, -1):
                current_price = sub.iloc[i]['unadjusted_close']
                next_split = sub.iloc[i + 1]['split'] or 1.0
                next_dividend = sub.iloc[i + 1]['dividend'] or 0.0
                
                # Update cumulative factor based on next period's events
                if next_split != 1.0:
                    cumulative_factor /= next_split
                if next_dividend > 0:
                    cumulative_factor *= (adjusted_prices[i + 1] - next_dividend) / adjusted_prices[i + 1]
                
                adjusted_prices[i] = round(current_price * cumulative_factor, 2)
            
            df.loc[mask, 'backward_adj_close'] = adjusted_prices
        
        return df
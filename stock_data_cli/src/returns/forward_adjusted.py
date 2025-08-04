class ForwardAdjusted:
    def __init__(self, data):
        self.data = data

    def forward_adj(self):
        df = self.data.copy()

        # sort: oldest -> newest
        df = df.sort_values(['ticker_symbol', 'datetime'], ascending=[True, True])
        
        for ticker in df['ticker_symbol'].unique():
            mask = df['ticker_symbol'] == ticker
            sub = df.loc[mask].copy()
            
            # Start from oldest
            adjusted_prices = [0] * len(sub)
            adjusted_prices[0] = sub.iloc[0]['unadjusted_close']  # First price unchanged
            
            cumulative_factor = 1.0
            
            for i in range(1, len(sub)):  # Start from second price
                current_price = sub.iloc[i]['unadjusted_close']
                prev_split = sub.iloc[i-1]['split'] or 1
                prev_dividend = sub.iloc[i-1]['dividend'] or 0
                
                # Update cumulative adjustment factor
                if prev_split != 1:
                    cumulative_factor *= prev_split
                if prev_dividend > 0:
                    # Add dividend reinvestment effect
                    cumulative_factor *= (1 + prev_dividend / adjusted_prices[i-1])
                    
                adjusted_prices[i] = round(current_price * cumulative_factor, 2)
            
            df.loc[mask, 'forward_adj_close'] = adjusted_prices
        
        return df
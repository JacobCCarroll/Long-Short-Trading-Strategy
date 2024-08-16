# Long-Short-Trading-Strategy
This is a simple, low-frequency long/short trading strategy I built on Nike and Footlocker stock.  

Trading Strategy: 
This strategy looks at the cumulative percent returns of Nike and Footlocker since 2019. When the cumulative returns diverge by more than 25%, it goes short the outperforming stock and goes long the underperforming stock. The short is covered when the cumulative returns converge again. 

Parameter Considerations: 
Going short at 25% divergence and covering at return convergence is a somewhat arbitrary choice. A wider interval would be triggered less frequently while a shorter interval would be triggered more frequently. A wider interval is a little bit more conservative. Another consideration is cumulative return since 2019. Changing this time also changes the cumulative returns of the respective stocks. 

P&L Summary:
Not including any transaction fees or short interest, this strategy generates $1635.80 on 5 $1000 long/short trades. 

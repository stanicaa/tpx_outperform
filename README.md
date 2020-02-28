# tpx_outperform
Identifying stocks that can potentially outperform Topix for 10 days.

There are 3 steps:
<li> Run the identify(f, t) function, where f is the file holding your stock prices, t holds the index prices, both shoudl have same time line as the index. This creates the basic data, a list with elements [stock, days], where stock is the code of the stock, and days is the number of underperforming days after which it can start outperforming TPX. Each stock is different, and each stock could have multiple values here. </li>
<li> select() and current() functions are being used to identify the potential opportunities/ideas as of now. As the same stock could be present in multiple list elements from above, the select() function gets only one element for each existing stock. </li>
<li> The function current() runs the results from select() above and checks which stocks have actually been underperforming for the number of days identified above. </li>

The algo is made specifically for the Japanese market, as the approach assumes a storng mean-reversion type of market. It is also made to help with discovering potential short term ideas - not necessarily to automatically trade anything that is picked by the algo.

The goal of the file is purely for research purposes - it doesn't work out of the box. You need to get your own market data. The program is built using Bloomberg data saved in an excel file, so any other data/file type will need to have the relevant functionality updated.

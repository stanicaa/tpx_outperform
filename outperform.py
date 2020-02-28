import pandas as pd
from pandas.tseries.offsets import BDay
import datetime

def bsd(a):
    isBusinessDay = BDay().onOffset
    match_series = pd.to_datetime(a.index).map(isBusinessDay) #bC is the DataFrame we work on
    a=a[match_series]
    a=a.astype(float)
    return a

def proc(t): #t here is the name of the excel file that holds the data for the Japanese market stocks
    fi=pd.read_excel(t, index_col=0) #skiprows=3 allows you to start at 3/4
    g=fi.drop(fi.index[0])
    return g

def price(t): #t here is the name of the excel file that holds the data for the Japanese market sectors indices
    fi=pd.read_excel(t, index_col=0) #skiprows=3 allows you to start at 3/4
    fi=fi.drop(fi.index[0])
    fi=fi.drop(fi.index[0])
    fi=fi.drop(fi.index[0])
    n=pd.DataFrame(index=fi.index)
    l=list(fi)
    for i in range(0,len(l),2):
        n[l[i]]=fi[l[i]]
    return n

def comps(stock, a, b): #a is the stock DF, b is the TPX df
    n=pd.DataFrame(index=a.index)
    n[stock]=a[stock]
    n['TPX']=b['TPX Index']
    n=n.astype(float)
    return n


def uwind(a, window, b):
    """
    the function searching for stocks outperforming over a certain period,
    then trying to identify which are the periods and the length of the interval
    after which it outperforms for xx days.
    a is the DF obtained above at comps(), b is the number of days to check for underperformance,
    window is the holding period for which it checks
    """
    ll=list(a)
    lt=a.index
    u_l=[]
    time_list=[]
    k=0
    while k<len(a)-1-window:
        if a[ll[0]].iloc[k:k+window].sum()>a[ll[1]].iloc[k:k+window].sum():
            time_list.append(a.index[k])
            k=k+window-1
        k+=1
    for j in time_list:
        for kk in range(len(lt)):
            if j==lt[kk]:
                if kk>b:
                    if a[ll[0]].iloc[kk-b:kk].sum()<a[ll[1]].iloc[kk-b:kk].sum():
                        u_l.append(kk)
    #print(len(u_l))
    ratio=len(u_l)/len(time_list)
    return (ratio, b, len(u_l))

def dwwind(a, window): #the windown here is the same as b variable above
    ll=list(a)
    time_list=[]
    k=0
    while k<len(a)-1-window:
        if a[ll[0]].iloc[k:k+window].sum()<a[ll[1]].iloc[k:k+window].sum():
            time_list.append(a.index[k])
            k=k+window-1
        k+=1
    #print(len(time_list))
    le=len(time_list)
    return le


#running the program for analysis of outperformance, only file names as input

def identify(f, t):
    bb=proc(f)
    bb=bsd(bb)
    cc=price(t)
    stocks=list(bb)
    candidates=[]
    for i in stocks: #running the functions below against each stock in the dataframe
        ss=comps(i, bb, cc)
        ssp=ss.pct_change()
        ssp=ssp.drop(ssp.index[0])
        print(i)
        for alpha in range(2, 60, 1):
            r, q, p=uwind(ssp, 10, alpha)
            if r>0.6:
                if p/dwwind(ssp,alpha)>0.9:
                    candidates.append([i,alpha])
    return candidates


def select(bp,bb):
    """
    bp is the stock DF with price changes, bb is the list from identify above.
    It only gets the shortest period of time per stock

    """
    cool=[]
    lb=list(bp)
    for i in lb:
        for j in bb:
            if j[0]==i:
                cool.append(j)
                break
    return cool

#The function is checking which companies are about to start outperforming TPX for 10 days
def current(cool):
    pqq=[]
    for m in cool:
        stock=m[0]
        v=m[1]
        if bp[stock].iloc[-v:].sum()<cp.iloc[-v:].sum():
            pqq.append(m)
    return pqq

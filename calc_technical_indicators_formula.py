# 威廉指标(WR)Williams Overbought/Oversold Index WR 威廉指标
def Williams(df,timeperiod=14):
    wr_indicator = [''] * (timeperiod - 1)
    for i in range(0, len(list(df['volume'])) - timeperiod + 1):
        stock = df[i:timeperiod + i]
        wr_row = (-100) * (max(stock['high']) - stock['close'][-1]) / (max(stock['high']) - min(stock['low']))
        wr_indicator.append(wr_row)
    df['WR'] = wr_indicator

# Stochastic Oscillator SO 随机振荡器
def Stochastic_Oscillator(df, timeperiod=14):
    so_indicator = [''] * ( timeperiod -1 )
    for i in range(0, len(list(df['volume'])) - timeperiod + 1 ):
        stock = df[i:timeperiod + i]
        so_row = 100 * (stock['close'][-1] - min(stock['low'])) / (max(stock['high']) - min(stock['low']))
        so_indicator.append(so_row)
    df['SO'] = so_indicator

# SMA均线
def SMA(df, timeperiod=15):
    sma_indicator = [''] * (timeperiod - 1)
    for i in range(len(df['volume'])-timeperiod+1):
        stock = df[i:timeperiod + i]
        sma_row = sum(stock['close'])/timeperiod
        sma_indicator.append(sma_row)
    df['SMA'] = sma_indicator

# Price Rate of Change PRC 价格波动率
def Price_Rate_of_Change(df, timeperiod=14):
    prc_indicator = [''] * ( timeperiod - 1)
    for i in range(0, len(list(df['volume'])) - timeperiod + 1 ):
        stock = df[i:timeperiod + i]
        prc_row= (stock['close'][-1] - stock['close'][0]) / (stock['close'][0])
        prc_indicator.append(prc_row)
    df['PRC'] = prc_indicator
    
# KDJ 随机指标
def KDJ(DM,date,days):
    days -=1
    C,L,H=[],[],[] #周期内每日收盘价,每日最低价,每日最高价
    K,D,J=[],[],[]
    RSV=[] #股票开盘日起每日RSV
    threshold=8 #判断金死叉的阈值
    data = ts.get_hist_data(DM)
    dateList = [i for i in data.index][::-1] #日期list
    C = [i for i in data['close'][::-1]] #第n日收盘价
    L = [i for i in data['low'][::-1]]
    H = [i for i in data['high'][::-1]]
    
    RSV.append((C[0]-L[0])/(H[0]-L[0])*100)
    for i in range(1,len(C)):
        if i<days:
            t=0
        else:
            t=i-days
        RSV.append((C[i]-min(L[t:i+1]))/(max(H[t:i+1])-min(L[t:i+1]))*100)
    
    for i in range(3):
        K.append(100)
        D.append(100)
        J.append(100)
    for i in range(3,len(C)):
        K.append(K[i-1]*2/3 + RSV[i]/3)
        D.append(D[i-1]*2/3 + K[i]/3)
        J.append(K[i]*3 - 2*D[i])
    
    #要获取的数据在Klist的索引
    index = dateList.index(str(datetime.strptime(date, "%Y-%m-%d"))[:10]) 
    print('股票代码:',DM,'日期：',date)
    K1=K[index]
    D1=D[index]
    J1=J[index]
    print('K:',round(K1,2))
    print('D:',round(D1,2))
    print('J:',round(J1,2))
    
    #买入卖出判断，-1看跌，1看涨，0持有
    if index<len(C)-1:
        if abs(J1-D1)<threshold: #近金叉或者死叉
            if J1-D1>threshold: 
                if J[index-1]-D[index-1]>J1-D1:
                    if C[index+1]<C[index]:
                        return -1,1
                    else:
                        return -1,0
                if J[index-1]-D[index-1]<threshold:
                    if C[index+1]>C[index]:
                        return 1,1
                    else:
                        return 1,0
                else:
                    return 0,0        
            else:
                print(-1)
                if C[index+1]<C[index]:
                    return -1,1
                else:
                    return -1,0
                        
        if J1>D1: #要涨，K线总是在中间,故简化
            print(1)
            if C[index+1]>C[index]:
                return 1,1
            else:
                return 1,0
                        
        elif J1<D1: #要跌
            print(-1)
            if C[index+1]<C[index]:
                return -1,1
            else:
                return -1,0
                    
        else:  #持有
            print(0)
            return 0,0
    return 0,0

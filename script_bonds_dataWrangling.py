##USING NOW
#duplicate issue
#pass numpy array

import pandas as pd
import os
import glob
from functools import reduce
import json
import numpy


# df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
#                         'B': ['B0', 'B1', 'B2', 'B3'],
#                         'C': ['C0', 'C1', 'C2', 'C3'],
#                         'D': ['D0', 'D1', 'D2', 'D3']},
#                  )
    

# df2 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
#                         'B': ['B3', 'B6', 'B3', 'B9'],
#                         # 'C': ['C0', 'C1', 'C2', 'C3'],
#                         'D': ['D0', 'D1', 'D2', 'D3']},
#                        )
    
# df3=pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
#                         'B': ['B8', 'B9', 'B10', 'B11'],
#                         'C': ['C8', 'C9', 'C10', 'C11'],
#                         'D': ['D8', 'D9', 'D10', 'D11']},
#                       )
    

# frames = []
# frames.append(df1)
# frames.append(df2)
# frames.append(df3)
# #frames = [df1, df2, df3]

# print(df1)
# print(df2)
# count = 0
# result = ''
# for i in range(0,len(frames),2): 
#   if i == 0:
#     result = pd.merge(frames[i],frames[i+1],on=["A"] , how="outer")
#   else:
    
#     result = pd.merge(result,frames[i], on=["A"] , how="outer")
 


# #result =  reduce(lambda x, y: pd.merge(x, y, on = ['A'], how="outer"), frames)
# print(result)



#------------------------------------------------------



#Variables
countryNamesSliced=[]
countries = []


path = os.getcwd()
extension = 'csv'
os.chdir(path)
countryNames = glob.glob('*.{}'.format(extension))
for countryName in countryNames:
    countryNamesSliced.append(countryName.split(" "))
for i in countryNamesSliced:
    if i[0] not in countries:
        countries.append(i[0])




dd = {}
for name in countries:
    tempCont = []
    for country in countryNames:
        if name in country:
            tempCont.append(country)
    dd[name] = tempCont
sorted(dd.items(), key=lambda x: x[0], reverse=False)

print(dd)



for key in dd:
  if key != "Germany":#or key=="Souht" or key="U.S."
    continue
  print("Working for {0} bonds".format(key))
  print("All Directories\n", dd[key])
  
  leng = len(dd[key])//2
  count = 0
  bonds=[]
  prev = numpy.array([])
  for i in range(0,leng):
    print(dd[key][count])
    print(dd[key][count+1],"loop")
    try:
      read2010 = pd.read_csv(dd[key][count])
      read1970 = pd.read_csv(dd[key][count+1])
      frames = [ read2010,read1970]
      
      # newArray = pd.concat(frames,ignore_index=True).to_numpy()
      # bonds.append(newArray)
      bonds.append(pd.concat(frames))
    except:
      bonds.append(pd.read_csv(dd[key][count+1]))
    
    # nn = numpy.append(prev,newArray)
    # prev = nn

    
    # pd.concat(frames,ignore_index=True).to_pickle("test{0}.pkl".format(i))
    # p +=1
    
    # print(len(bonds))
    # print(bonds)
    # break

    count+=2
    
  # print(prev)
  

    
  
  print(len(bonds))
  # df = []

  # print("In loop")
  # series=[]
  # for i in bonds:
  #   f = pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"])
  #   series.append(f)

  # for i in range(p):

  #   df.append(pd.read_pickle("test{0}.pkl".format(i)))
      #  bonds = json.load(fp)
  #print(bonds)
  # print(prev)
  # print(pd.DataFrame(prev))
  print("Merging")
  # result = pd.merge( [pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"]) for i in bonds][0], [pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"]) for i in bonds][2], how="outer",on=["Date"])
 
  #----------------------
  # listy = [pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"]) for i in bonds]
  # dfs = [df.set_index('Date') for df in listy]
  # print(dfs)

  # print(pd.concat(dfs, axis=1, verify_integrity=False).reset_index())
  # break

 #--------------------------------
 
  # x = pd.DataFrame(bonds[0], columns=['Date', 'Price', "Open", "High","Low", "Change %"])
  # y = pd.DataFrame(bonds[1], columns=['Date', 'Price', "Open", "High","Low", "Change %"])
  # z = pd.DataFrame(bonds[2], columns=['Date', 'Price', "Open", "High","Low", "Change %"])

  # n = pd.DataFrame.drop_duplicates(pd.merge(x,y,on="Date",how="outer"))
  # print(n)
  # break
  # print(listy[0])
  # print(type(listy))
 
  if len(bonds) == 2:
    result = pd.DataFrame.drop_duplicates(pd.merge(bonds[0],bonds[1],on=["Date"] , how="outer"))
  elif len(bonds) == 1:
    result = bonds[0]
  else:
    try:
      result = ''
      for i in range(0,len(bonds),2): 
        if i == 0:
          result = pd.DataFrame.drop_duplicates(pd.merge(bonds[i],bonds[i+1],on=["Date"] , how="outer"))
        else:
          
          result = pd.DataFrame.drop_duplicates(pd.merge(result,bonds[i], on=["Date"] , how="outer"))
    except:
      continue
  

#--------------------------------

  #print([pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"]).set_index("Date", inplace = True) for i in bonds])
 # result = pd.DataFrame.drop_duplicates(reduce(lambda x, y: pd.merge(x, y, on = ['Date'], how="outer"), [pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"]) for i in bonds]))
  print("Merged")

  # os.remove("test{0}.pkl".format(i))
  print(result)
  
  

  

  try:
    result = pd.DataFrame.drop_duplicates(result)
  except:
    pass


  # chunksize = 10 ** 6
  # for chunk in pd.DataFrame(result, chunksize=chunksize):
  #   pd.DataFrame.drop_duplicates(chunk)
 

  result['Date'] =pd.to_datetime(result.Date)
  

  sorted_df = result.sort_values(by='Date',axis=0,ascending=False)
 
  sorted_df["Date"]=sorted_df.Date.dt.strftime('%b %d, %y')

  path = os.getcwd()+"/AOutput/"
  realPath = os.getcwd()
  os.chdir(path)

  try:
    sorted_df.style.highlight_null().to_excel('{0}.xlsx'.format(key), engine='openpyxl',index=False)
  except:
    sorted_df.to_excel('{0}.xlsx'.format(key), engine='openpyxl',index=False)

  os.chdir(realPath)
    

  


exit()




#--------------------------
read1970 = pd.read_csv("Australia 6-Year Bond Yield Historical Data (1).csv")
read2010 = pd.read_csv("Australia 6-Year Bond Yield Historical Data (2).csv")
frames = [ read2010,read1970]
bond1 = pd.concat(frames,ignore_index=True)

read1970 = pd.read_csv("Australia 5-Year Bond Yield Historical Data (3).csv")
read2010 = pd.read_csv("Australia 5-Year Bond Yield Historical Data (4).csv")
frames = [ read2010,read1970]
bond2 = pd.concat(frames,ignore_index=True)

def highlight_cells():
    # provide your criteria for highlighting the cells here
    return ['background-color: yellow']
bond2.style.apply(highlight_cells)


result = pd.merge(bond1, bond2, how="outer",on=["Date"])
result = pd.DataFrame.drop_duplicates(result)
print(result.head())




result['Date'] =pd.to_datetime(result.Date)

sorted_df = result.sort_values(by='Date',axis=0,ascending=False)
sorted_df["Date"]=sorted_df.Date.dt.strftime('%b %d, %y')

sorted_df.style.highlight_null().to_excel('styled.xlsx', engine='openpyxl',index=False)



#sorted_df.to_csv("resultt.csv",index=False )



exit()

df1 = pd.DataFrame({'A': [ 'Jan 16, 2005','Jun 16, 1989','Jan 30, 1980', 'Jan 16, 1980', ],
                        'B': ['B0', 'B1', 'B2', 'B3'],
                        'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1', 'D2', 'D3']},
                 )
    

df2 = pd.DataFrame({'A': ['Oct 20, 2020', 'Jan 10, 2019', 'Jul 12, 2008', 'Jun 16, 1989'],
                        'B': ['B4', 'B5', 'B6', 'B7'],
                        'C': ['C4', 'C5', 'C6', 'C7'],
                        'D': ['D4', 'D5', 'D6', 'D7']},
                       )
    
df3=pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                        'B': ['B8', 'B9', 'B10', 'B11'],
                        'C': ['C8', 'C9', 'C10', 'C11'],
                        'D': ['D8', 'D9', 'D10', 'D11']},
                      )
    


result = pd.merge(df1, df2, how="outer",on=["A"])
print(result["A"])

result['A'] =pd.to_datetime(result.A)


sorted_df = result.sort_values(by='A',axis=0,ascending=False)
print(sorted_df)

sorted_df["A"]=sorted_df.A.dt.strftime('%b %d, %y')
print(sorted_df)

sorted_df.style.highlight_null('red')


sorted_df.to_csv("result.csv")

exit()

df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3'],
                        'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1', 'D2', 'D3']},
                 )
    

df2 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A4'],
                        'B': ['B4', 'B5', 'B6', 'B7'],
                        'C': ['C4', 'C5', 'C6', 'C7'],
                        'D': ['D4', 'D5', 'D6', 'D7']},
                       )
    
df3=pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                        'B': ['B8', 'B9', 'B10', 'B11'],
                        'C': ['C8', 'C9', 'C10', 'C11'],
                        'D': ['D8', 'D9', 'D10', 'D11']},
                      )
    

frames = [df1, df2, df3]

result = pd.concat(frames,verify_integrity=True)


read1970 = pd.read_csv("Australia 6-Year Bond Yield Historical Data (1).csv")
read2010 = pd.read_csv("Australia 6-Year Bond Yield Historical Data (2).csv")


print(read1970.head())
print(read1970.shape,read2010.shape)


frames = [ read2010,read1970]

result = pd.concat(frames,ignore_index=True)

print(result.tail())

result.to_csv("new2.csv")













#-----------------------BACKUP----------
# read1970 = pd.read_csv("Australia 6-Year Bond Yield Historical Data (1).csv")
# read2010 = pd.read_csv("Australia 6-Year Bond Yield Historical Data (2).csv")
# frames = [ read2010,read1970]
# bond1 = pd.concat(frames,ignore_index=True)

# read1970 = pd.read_csv("Australia 5-Year Bond Yield Historical Data (3).csv")
# read2010 = pd.read_csv("Australia 5-Year Bond Yield Historical Data (4).csv")
# frames = [ read2010,read1970]
# bond2 = pd.concat(frames,ignore_index=True)

# def highlight_cells():
#     # provide your criteria for highlighting the cells here
#     return ['background-color: yellow']
# bond2.style.apply(highlight_cells)


# result = pd.merge(bond1, bond2, how="outer",on=["Date"])
# result = pd.DataFrame.drop_duplicates(result)
# print(result.head())




# result['Date'] =pd.to_datetime(result.Date)

# sorted_df = result.sort_values(by='Date',axis=0,ascending=False)
# sorted_df["Date"]=sorted_df.Date.dt.strftime('%b %d, %y')

# sorted_df.style.highlight_null().to_excel('styled.xlsx', engine='openpyxl',index=False)



# #sorted_df.to_csv("resultt.csv",index=False )



# exit()


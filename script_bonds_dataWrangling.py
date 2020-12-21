##USING NOW
#duplicate issue
#pass numpy array

import pandas as pd
import os
import glob
from functools import reduce
import json
import numpy


df1 = pd.DataFrame({'A': [0,2,3,5],
                        'B': [2,3,4,5],
}
                 )
    

df2 = pd.DataFrame({'A': [2,4,3,5],
                        'B': [1,2,3,4],
}
                       )
    
df3=pd.DataFrame({'A': [1,2,3,4],
                        'B': [6,7,8,9],
}
                      )
df4=pd.DataFrame({'A': [1,2,3,5],
                        'B': [6,3,2,0],
}
                      )

df5=pd.DataFrame({'A': [1,2,3,5],
                        'B': [6,3,2,0],
}
                      )
df6=pd.DataFrame({'A': [1,2,3,5],
                        'B': [6,3,2,0],
}
                      )
newframes = [df1,df2,df3,df4,df5,df6]

# df1 = df1.set_index("A")
# df2 = df2.set_index("A")
# df3 = df3.set_index("A")
# df4 = df4.set_index("A")
frames = []
for i in range(0,len(newframes)):
  frames.append(newframes[i].set_index("A"))



# x=pd.DataFrame({'A': [2,6,7,8,41,9,4,8],
#                         'B': [6,7,8,9],
# }
#                       )
# y=pd.DataFrame({'A': [2,6,7,8,41,9,4,8],
#                         'B': [6,7,8,9],
# }
#                       )


# df1sub = df1.loc[:, df1.columns != 'A']
# df2sub = df2.loc[:, df2.columns != 'A']
# df3sub = df3.loc[:, df3.columns != 'A']
# xsub = x.loc[:, x.columns != 'A']
# ysub = y.loc[:, y.columns != 'A']


# x["B"] = df2["B"]-df1["B"]
# y["B"] = df3["B"] - x["B"]
# print(x)
# print(y)

# xsub = df2sub-df1sub
# ysub = df3sub - xsub
# print(x)
# print(y)
x = df2 - df1
y = df3  - x

# lst = [1,6,2,8,3,4]
# res = [y-x for x, y in zip(lst, lst[1:])]    
# print(res)  # [-5, 4, -6, 5, -1]


# fr = [y-x for x, y in zip(frames, frames[1:])]
# print(fr)



# if len(frames) % 2 == 0:
#   for i in range(0,len(frames),4):  
#     x = frames[i+1] - frames[i]
#     y = frames[i+2] - x
#     v = pd.merge(x,y ,on = "A", how="outer")
    
#     z = y - [i+3]
#     v = pd.merge(v,z ,on = "A", how="outer")

# else:

#   for i in range(0,len(frames),3):
    
#       x = frames[i+1] - frames[i]
#       y = frames[i+2] - x
#       v = pd.merge(x,y ,on = "A", how="outer")


# print(v)
# print(x,"\n")
# print(y,"\n")

#print(v)



    

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

# print(dd)

path = os.getcwd()
extension = 'xlsx'
os.chdir(path+"/BOutput/")
doneBCont = glob.glob('*.{}'.format(extension))
doneBCont = [i.replace(".xlsx","") for i in doneBCont]
print(doneBCont)


os.chdir(path)

for key in dd:
  if key in doneBCont:
    continue
  # if key =="Argentina":
  #   continue
  print("Working for {0} bonds".format(key))
  print("All Directories\n", dd[key])
  
  leng = len(dd[key])//2
  count = 0
  nbonds=[]
  c = 1
  prev = numpy.array([])
  for i in range(0,leng):
    print(dd[key][count])
    print(dd[key][count+1],"loop")
    try:
      read2010 = pd.read_csv(dd[key][count])
      read1970 = pd.read_csv(dd[key][count+1])
      read2010l = [float(i[:-1].replace(",","")) for i in read2010["Change %"]]
      read2010["Change %"] = pd.DataFrame(read2010l, columns=["Change %"])
      # read2010o = [float(i[:-1].replace(",","")) for i in read2010["Open"]]
      # read2010["Open"] = pd.DataFrame(read2010o, columns=["Open"])
      # read2010h = [float(i[:-1].replace(",","")) for i in read2010["High"]]
      # read2010["High"] = pd.DataFrame(read2010h, columns=["High"])

      read1970l = [float(i[:-1].replace(",","")) for i in read1970["Change %"]]
      read1970["Change %"] = pd.DataFrame(read1970l, columns=["Change %"])
      # read1970o = [float(i[:-1].replace(",","")) for i in read1970["Open"]]
      # read1970["Open"] = pd.DataFrame(read1970o, columns=["Open"])
      # read1970h = [float(i[:-1].replace(",","")) for i in read1970["High"]]
      # read1970["High"] = pd.DataFrame(read1970h, columns=["High"])
      frames = [ read2010,read1970]
    
    # newArray = pd.concat(frames,ignore_index=True).to_numpy()
    # bonds.append(newArray)


      nbonds.append(pd.concat(frames))
      # bfAppend = pd.concat(frames)
      # bfAppend = bfAppend.rename(columns={'Price':'Price{0}'.format(c),
      # 'Change %':'Change %{0}'.format(c),'High':'High{0}'.format(c),
      # 'Low':'Low{0}'.format(c),'Open':'Open{0}'
      #                     })
      # nbonds.append(bfAppend)


    # read2010["Change %"] = pd.to_numeric(read2010['Change %'], errors='coerce')
    # print(read2010.fillna(0))
    # exit()
  
    
    # read1970["Change %"] = read1970["Change %"][0:-1]
    # read2010["Change %"] = read2010["Change %"][0:-1]
    # frames = [ read2010,read1970]
    
    # newArray = pd.concat(frames,ignore_index=True).to_numpy()
    # bonds.append(newArray)
    # nbonds.append(pd.concat(frames))
    #print(nbonds)
    except:
      read1970 = pd.read_csv(dd[key][count+1])
      read1970l = [float(i[:-1].replace(",","")) for i in read1970["Change %"]]
      read1970["Change %"] = pd.DataFrame(read1970l, columns=["Change %"])
      # read1970o = [float(i[:-1].replace(",","")) for i in read1970["Open"]]
      # read1970["Open"] = pd.DataFrame(read1970o, columns=["Open"])
      # read1970h = [float(i[:-1].replace(",","")) for i in read1970["High"]]
      # read1970["High"] = pd.DataFrame(read1970h, columns=["High"])
      
      nbonds.append(read1970)
      # bfAppend = read1970.rename(columns={'Price':'{0}Price'.format(c),
      # 'Change %':'{0}Change %'.format(c)
      #                     })
      # nbonds.append(bfAppend)


    count+=2
    c+=1


    

    
    # nn = numpy.append(prev,newArray)
    # prev = nn

    
    # pd.concat(frames,ignore_index=True).to_pickle("test{0}.pkl".format(i))
    # p +=1
    
    # print(len(bonds))
    # print(bonds)
    # break

     
    
  # print(prev)
  

    
  
  # print(len(bonds))
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



  # print(nbonds)
  # x = pd.merge(nbonds[0],nbonds[1], how="outer")
  # print(x)
  # exit()
 

  bonds = []
  for i in range(0,len(nbonds)):
    # [x for x in nbonds[i]]
    # try:
    #   nbonds[i]["Open"] = pd.to_numeric(nbonds[i]["Open"].astype(str).str.replace(',',''))
    #   nbonds[i]["High"] = pd.to_numeric(nbonds[i]["High"].astype(str).str.replace(',',''))
      
      
    # except:
    #    readh = [float(str(x.replace(",",""))) for x in nbonds[i]["Open"]]
    #    nbonds[i]["Open"] = pd.DataFrame(readh, columns=["Open"])
    # try:
    #   nbonds[i]["High"] = pd.to_numeric(nbonds[i]["High"])
    # except:
    #   readh = [float(x.replace(",","")) for x in nbonds[i]["High"]]
    #   nbonds[i]["High"] = pd.DataFrame(readh, columns=["High"])
   
      
    # print("Looped")
    nbonds[i] = nbonds[i].set_index("Date")
    nbonds[i] = nbonds[i].apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',','')))
    bonds.append(nbonds[i])

  


  
  # print(type(bonds[0]["Price"][0]), type(bonds[0]["Change %"][0]),type(bonds[0]["High"][0]),type(bonds[0]["Low"][0]),type(bonds[0]["Open"][0]))
  #print(type(bonds[-1]["Price"][0]), type(bonds[1]["Change %"][0]),type(bonds[-1]["Open"][-1]),type(bonds[-1]["High"][-1]))
  
  # for i in range(len(bonds)):
  #   for x in range(len(bonds[i])):
  #     print(type(bonds[i]["Change %"][x]))
    
  #exit()

  # print(bonds[0],bonds[1])
  # print(bonds[0]-bonds[1])
  

  bonds = [i for i in bonds]
  

  bonds = [pd.DataFrame.drop_duplicates(y.sub(x, fill_value=0)) for x, y in zip(bonds, bonds[1:])]

  print("ORDER CHANGED HERE")
  # print(bonds)
  
  for i in range(0,len(bonds)):
    bonds[i] = bonds[i].rename(columns={'Price':'Price{0}'.format(i),
      'Change %':'Change %{0}'.format(i),'High':'High{0}'.format(i),
      'Low':'Low{0}'.format(i),'Open':'Open{0}'.format(i)
                          })
  

  
 
  if len(bonds) == 2:
    result = pd.DataFrame.drop_duplicates(pd.merge(bonds[0],bonds[1],on=["Date"] , how="outer"))
    result = result.fillna(0)
    # print(result)
    
  elif len(nbonds) == 1:
    result = nbonds[0]
  else:
    
    result = ''
    for i in range(0,len(bonds),2):
      
      if i == 0:
        result = pd.DataFrame.drop_duplicates(pd.merge(bonds[i],bonds[i+1],on=["Date"] , how="outer"))
        result = result.fillna(0)
      else:
        
        result = pd.DataFrame.drop_duplicates(pd.merge(result,bonds[i], on=["Date"] , how="outer"))
        result = result.fillna(0)
        # print(result)
  
      

        
  
  

#--------------------------------

  #print([pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"]).set_index("Date", inplace = True) for i in bonds])
 # result = pd.DataFrame.drop_duplicates(reduce(lambda x, y: pd.merge(x, y, on = ['Date'], how="outer"), [pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"]) for i in bonds]))
  print("Merged")

  # os.remove("test{0}.pkl".format(i))
  
  
  

  # print(result)

  try:
    result = pd.DataFrame.drop_duplicates(result)
  except:
    pass



  # chunksize = 10 ** 6
  # for chunk in pd.DataFrame(result, chunksize=chunksize):
  #   pd.DataFrame.drop_duplicates(chunk)
  # print(result.columns)
  # print(result.columns[0:-1:5])
  # print(result.columns[1:-1:5])
  # print(result.columns[2:-1:5])
  # print(result.columns[3:-1:5])
  # print(result.columns[4::5])

  

  x = result.columns[0:-1:5]
  y = result.columns[1:-1:5]
  z = result.columns[2:-1:5]
  a = result.columns[3:-1:5]
  b = result.columns[4::5]
  
  xy = list(x)+list(y)+list(z)+list(a)+list(b)
  print(xy)
  result = result[xy]


  # print(result)

  # exit()




  # result = result.concat(result[result.columns[1:-1:5]])
  # result = result(sorted(result.columns, key=lambda x: result.columns[x:-1:5]), axis=1)




 
  #result = sorted((result.columns, key=lambda x: x[::-2]), axis=1)

  # print(result)
  # exit()
  
  result = result.reset_index()

  result['Date'] =pd.to_datetime(result.Date)

  

  sorted_df = result.sort_values(by='Date',axis=0,ascending=False)
 
  sorted_df["Date"]=sorted_df.Date.dt.strftime('%b %d, %y')

  path = os.getcwd()+"/BOutput/"
  realPath = os.getcwd()
  os.chdir(path)

  print(sorted_df,"...")

  

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


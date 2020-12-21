##USING NOW


import pandas as pd
import os
import glob
from functools import reduce
import json
import numpy
import re
from styleframe import StyleFrame, Styler, utils




#Variables
countryNamesSliced=[]
countries = []


path = os.getcwd()
extension = 'csv'
os.chdir(path)
countryNames = glob.glob('*.{}'.format(extension))


# print("OK till here")
# for countryName in countryNames:
#     # x = re.search("([a-zA-Z]+ [^Overnighta-zA-Z]*)(\d*.+ Bond)", countryName)
#     # print(x.group(1))
#     # # exit()
#     # countryNamesSliced.append(x)
#     countryNamesSliced.append(countryName.split(" "))
# for i in countryNamesSliced:
#     if i[0] not in countries:
#         countries.append(i[0])

# print("Changed Here")
# print(countries)

countries =['Argentina', 'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Belgium', 'Botswana', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'China', 'Colombia', 'Croatia', 
'Cyprus', 'Czech', 'Egypt', 'France', 'Germany', 'Greece', 'Hong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kenya',
 'Malaysia', 'Malta', 'Mauritius', 'Mexico', 'Morocco', 'Namibia', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar',
  'Romania', 'Russia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'Souht Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'Uganda', 'Ukraine',
   'United Kingdom', 'United States', 'Vietnam']




dd = {}
for name in countries:
    tempCont = []
    for country in countryNames:
        if name in country:
            tempCont.append(country)
            
    dd[name] = tempCont




sorted(dd.items(), key=lambda x: x[0], reverse=False)





path = os.getcwd()
extension = 'xlsx'
if not os.path.exists('Output'):
    os.makedirs('Output')
os.chdir(path+"/Output/")
doneBCont = glob.glob('*.{}'.format(extension))
doneBCont = [i.replace(".xlsx","") for i in doneBCont]
# print(doneBCont)


os.chdir(path)



def atoi(text):
    return (int(text) if text.isdigit() else text)
def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]


#-------------


for key in dd:
  # print(key)
  # continue
  if key in doneBCont:
    continue
  # if key != "United":
  #   continue

  dd[key].sort(key=natural_keys)


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


      read1970l = [float(i[:-1].replace(",","")) for i in read1970["Change %"]]
      read1970["Change %"] = pd.DataFrame(read1970l, columns=["Change %"])
  
      frames = [ read2010,read1970]



      nbonds.append(pd.concat(frames))
   
    except:
      read1970 = pd.read_csv(dd[key][count+1])
      read1970l = [float(i[:-1].replace(",","")) for i in read1970["Change %"]]
      read1970["Change %"] = pd.DataFrame(read1970l, columns=["Change %"])

      
      nbonds.append(read1970)



    count+=2
    c+=1


    

  
  print("Merging")
  print("Not Changed")
  

  bonds = []
  for i in range(0,len(nbonds)):

    nbonds[i] = nbonds[i].set_index("Date")
    nbonds[i] = nbonds[i].apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',','')))
    bonds.append(nbonds[i])

  print(len(bonds))
  

  


 
  newBonds = []

  for i in range(0,len(bonds)):
    if i == 0:
      continue
    else:
      # print("LOOP\n",i)
      x = bonds[i].sub(bonds[0],fill_value=0)
      x = x[~x.index.duplicated()]

      xl = x.add(bonds[0],fill_value=0)
      xl = xl[~xl.index.duplicated()]

      mdxl = xl.replace(0.0, numpy.nan)
      mdxl = mdxl[~mdxl.index.duplicated()]

      yl = bonds[i].sub(x,fill_value=0)
      yl = yl[~yl.index.duplicated()]

      xfl = mdxl.sub(yl,fill_value=numpy.nan)
      xfl = xfl[~xfl.index.duplicated()]

      newBonds.append(xfl)


  
    
  bonds = []

  bonds = newBonds.copy()

  print(len(bonds))
  print("Not Changed") 


  #--------------------------------------------------

  # print("ORDER CHANGED HERE")
  # print(bonds)


  c=0
  for x in range(0,len(bonds)):
        if x == 0:

          bonds[x] = bonds[x].rename(columns={'Price':'Treasory Spread On Price_{0}'.format(dd[key][x+3]),
            'Change %':'Treasory Spread On Change %_{0}'.format(dd[key][x+3]),'High':'Treasory Spread On High_{0}'.format(dd[key][x+3]),
            'Low':'Treasory Spread On Low_{0}'.format(dd[key][x+3]),'Open':'Treasory Spread On Open_{0}'.format(dd[key][x+3])
                                })
          c = x+3
        else:
          new = c+2
          bonds[x] = bonds[x].rename(columns={'Price':'Treasory Spread On Price_{0}'.format(dd[key][new]),
            'Change %':'Treasory Spread On Change %_{0}'.format(dd[key][new]),'High':'Treasory Spread On High_{0}'.format(dd[key][new]),
            'Low':'Treasory Spread On Low_{0}'.format(dd[key][new]),'Open':'Treasory Spread On Open_{0}'.format(dd[key][new])
                                })
          c = new


 

  print("Not Changed")



 
  if len(bonds) == 2:
    result = pd.DataFrame.drop_duplicates(pd.merge(bonds[0],bonds[1],on=["Date"] , how="outer"))
    result = result.fillna(value="na")
    # print(result)
    # exit()
    
  elif len(nbonds) == 1:
    result = nbonds[0]
  else:
    
    result = ''
    for i in range(0,len(bonds)):  #for i in range(0,len(bonds),2):
      
      if i == 0:
        result = pd.DataFrame.drop_duplicates(pd.merge(bonds[i],bonds[i+1],on=["Date"] , how="outer"))
        result = result.fillna(value="na")
      elif i == 1:
        continue
      else:
        
        result = pd.DataFrame.drop_duplicates(pd.merge(result,bonds[i], on=["Date"] , how="outer"))
        result = result.fillna(value="na")
        # print(result)

  print("Changed")

  # print(result.columns)

  # exit()
 
  


  #----------------------
  bonxs = [i for i in nbonds]


  
  # for i in range(0,len(bonxs)):
  #  for x in range(0,len(dd[key]),2):
  print(len(bonxs))
  c=0
  for x in range(0,len(bonxs)):
        if x == 0:

          bonxs[x] = bonxs[x].rename(columns={'Price':'Price_{0}'.format(dd[key][x+1]),
            'Change %':'Change %_{0}'.format(dd[key][x+1]),'High':'High_{0}'.format(dd[key][x+1]),
            'Low':'Low_{0}'.format(dd[key][x+1]),'Open':'Open_{0}'.format(dd[key][x+1])
                                })
          c = x+1
        else:
          new = c+2
          bonxs[x] = bonxs[x].rename(columns={'Price':'Price_{0}'.format(dd[key][new]),
            'Change %':'Change %_{0}'.format(dd[key][new]),'High':'High_{0}'.format(dd[key][new]),
            'Low':'Low_{0}'.format(dd[key][new]),'Open':'Open_{0}'.format(dd[key][new])
                                })
          c = new

        

  

  if len(bonxs) == 2:
    resulx = pd.DataFrame.drop_duplicates(pd.merge(bonxs[0],bonxs[1],on=["Date"] , how="outer"))
    # resulx = resulx.fillna(0)
    
    # print(result)
    
  elif len(bonxs) == 1:
    resulx = bonxs[0]
  else:
    
    resulx = ''
    for i in range(0,len(bonxs)):
      
      if i == 0:
        resulx = pd.DataFrame.drop_duplicates(pd.merge(bonxs[i],bonxs[i+1],on=["Date"] , how="outer"))
        # print(resulx,"jkljhk")
        # exit()
   
        # resulx = resulx.fillna(0)
      elif i == 1:
        continue
      else:
        # print(resulx, bonxs[i])
        
        resulx = pd.DataFrame.drop_duplicates(pd.merge(resulx,bonxs[i], on=["Date"] , how="outer"))
        # resulx = resulx.fillna(0)
    
  #pd.set_option('display.max_columns', None)
  # t = resulx.columns[0:5]
  b = resulx.columns[:]
  # resulx[t] =  resulx[t].fillna(value=0)
  resulx[b] =  resulx[b].fillna(value="na")

  # print(resulx)
  
        
        
  
  
      

        
  
  

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



  

  x = result.columns[0:-1:5]
  y = result.columns[1:-1:5]
  z = result.columns[2:-1:5]
  a = result.columns[3:-1:5]
  b = result.columns[4::5]
  
  xy = list(x)+list(y)+list(z)+list(a)+list(b)
  # print(xy)
  result = result[xy]
  print("Changed till here")

#---------------------

  x = resulx.columns[0:-1:5]
  y = resulx.columns[1:-1:5]
  z = resulx.columns[2:-1:5]
  a = resulx.columns[3:-1:5]
  b = resulx.columns[4::5]
  
  xy = list(x)+list(y)+list(z)+list(a)+list(b)
  # print(xy)
  resulx = resulx[xy]


 
  
  result = result.reset_index()

  result['Date'] =pd.to_datetime(result.Date)

  

  sorted_df = result.sort_values(by='Date',axis=0,ascending=False)
 
  sorted_df["Date"]=sorted_df.Date.dt.strftime('%b %d, %y')

  # path = os.getcwd()+"/COutput/"
  # realPath = os.getcwd()
  # os.chdir(path)

  print(sorted_df,"...")
  



  #--------------------
  resulx = resulx.reset_index()

  resulx['Date'] =pd.to_datetime(resulx.Date)

  

  sortex_df = resulx.sort_values(by='Date',axis=0,ascending=False)
 
  sortex_df["Date"]=sortex_df.Date.dt.strftime('%b %d, %y')

  path = os.getcwd()+"/Output/"
  realPath = os.getcwd()
  os.chdir(path)

  print(sortex_df,"...")

  print("Sorted By Date")

  #--------------



  # pd.set_option('display.max_colwidth', None)
  sortex_df.columns = sortex_df.columns.str.replace('.csv', '')
  sorted_df.columns = sorted_df.columns.str.replace('.csv', '')

  print("Replaced String")
  

  sortex_df = StyleFrame(sortex_df, Styler(shrink_to_fit=False, wrap_text=False))
  sortex_df.set_column_width(sortex_df.columns,12) 
  writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))

  sorted_df = StyleFrame(sorted_df, Styler(shrink_to_fit=False, wrap_text=False))
  sorted_df.set_column_width(sorted_df.columns,12) 

  print("Stylesheet Created")


  
  # writer = pd.ExcelWriter('{0}.xlsx'.format(key))
  sortex_df.to_excel(writer,'Merging By Date',index=False)
  sorted_df.to_excel(writer,'Treasury Spread',index=False)
 
  writer.save()





  os.chdir(realPath)






  


exit()


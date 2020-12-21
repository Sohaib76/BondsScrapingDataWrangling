##Imports


import pandas as pd
import os
import glob
from functools import reduce
import json
import numpy
import re
from styleframe import StyleFrame, Styler, utils
import csv
import time
import pycountry
import math



# x = pycountry.countries.get(alpha_2='KR')
# print(x)
# exit()
# #Vietnam


#Defining Paths
main_path = os.getcwd()
output_path = main_path + "/Output/"
production_ouput_path = main_path + "/Production_Output/"
shortlist_output_path = main_path + "/Shortlist_Output/"
shortlist_production_ouput_path = main_path + "/Shortlist_Production_Output/"
quarterly_path = main_path + "/Quarterly_Insights/"
imputed_quarterly_path = main_path + "/Imputed_Quarterly_Insights/"
input_path_treasury = main_path + "/TREASURY_SPREADS_AND_YIELDS/"
if not os.path.exists('Output'):
      os.makedirs('Output')
if not os.path.exists('Production_Output'):
      os.makedirs('Production_Output')
if not os.path.exists('Shortlist_Output'):
      os.makedirs('Shortlist_Output')
if not os.path.exists('Shortlist_Production_Output'):
      os.makedirs('Shortlist_Production_Output')
if not os.path.exists('Quarterly_Insights'):
      os.makedirs('Quarterly_Insights')
if not os.path.exists("Imputed_Quarterly_Insights"):
      os.makedirs("Imputed_Quarterly_Insights")


#Renaming Conflict Names
os.chdir(input_path_treasury)
try: 
  os.rename(r'Souht Africa 12 Year Bond Yield Historical Data (1).csv',r'South Africa 12-Year Bond Yield Historical Data (1).csv')
  os.rename(r'Souht Africa 12 Year Bond Yield Historical Data.csv',r'South Africa 12-Year Bond Yield Historical Data.csv')
except:
  print("Already Renamed South Africa")
try:
  os.rename(r'U.S. 20-Year Bond Yield Bond Yield Historical Data (1).csv',r'United States 20-Year Bond Yield Historical Data (1).csv')
  os.rename(r'U.S. 20-Year Bond Yield Bond Yield Historical Data.csv',r'United States 20-Year Bond Yield Historical Data.csv')
except:
  print("Already Renamed")

os.chdir(main_path)

#Extensions
csv_extension = 'csv'
xlsx_extension ="xlsx"

#Global Var
os.chdir(main_path)
os.chdir(input_path_treasury)
countryNames = glob.glob('*.{}'.format(csv_extension))
os.chdir(main_path)


#Short Funcs
def atoi(text):
        return (int(text) if text.isdigit() else text)
def natural_keys(text):
        return [ atoi(c) for c in re.split('(\d+)',text) ]
def writeToCsv(input_list,name):
  os.chdir(main_path)
  os.chdir(production_ouput_path)
  f = open(name, 'a+',newline='')
  with f:
        writer = csv.writer(f)
        # writer.writerow(["Name", "Abbreviation"])
        writer.writerows(input_list)
  os.chdir(main_path)




#Function To Create adict.csv file containing starting and ending date.
def createADic():
    global countryNames
    
    os.chdir(main_path)
    
    countryNames.sort(key=natural_keys)

    os.chdir(output_path)
    f = open('adict.csv', 'w',newline='')
    with f:
        writer = csv.writer(f)
        writer.writerow(["Countries","1st starting date","1st ending date","2nd starting date","2nd ending date"])
    os.chdir(input_path_treasury)

    rowToWrite = []
    rowOfrows = []
    count = 0
    for countryName in countryNames:
        count += 1
        if count == 3:
            rowOfrows.append(rowToWrite)
            rowToWrite = []
            count = 1
        if count < 3:
            rowList = []
            with open(countryName, newline='', encoding='latin-1') as f: 
                reader = csv.reader(f)
                for row in reader:
                    rowList.append(row)

            try:
                endDate = rowList[1][0]
                startDate = rowList[-1][0]
            except:
                continue

            if count != 2:
                rowToWrite.append(countryName.replace(" (1)", ""))
                rowToWrite.append(startDate)
                rowToWrite.append(endDate)

            else:
            
                rowToWrite.insert(1,startDate)
                rowToWrite.insert(2,endDate)
                

        

            
        if countryNames.index(countryName)==len(countryNames)-1:
            
            rowOfrows.append(rowToWrite)
        
    os.chdir(main_path)
    os.chdir(output_path)
    f = open('adict.csv', 'a+',newline='')
    with f:
        writer = csv.writer(f)
        writer.writerows(rowOfrows)
    os.chdir(main_path)


# p = input("Do you want to create adic.csv ? Enter y/n  ")
# if p == "y":
#Uncomment
# createADic()


def getCountryAbbr(input_country):
    countries = {}
    for country in pycountry.countries:
          countries[country.name] = country.alpha_2
      
    if input_country == "Vietnam":
      input_country = "Viet Nam"
    elif input_country == "Czech Republic":
      input_country = "Czechia"
    elif input_country == "Russia":
      input_country = "Russian Federation"
    elif input_country == "South Korea":
      input_country = "Korea, Republic of"
    elif input_country == "Taiwan":
      input_country = "Taiwan, Province of China"
    code = countries.get(input_country, 'Unknown code')
    return code


def renameCountry(input_name,over):    
        if "Treasury Spread" in input_name and "Overnight" not in input_name:
            x = re.search("Of (.+)_(.+) (\d+)-*(.+)", input_name)
            field = x.group(1)[0]
            country = getCountryAbbr(x.group(2))
            yearOrmonthVal = x.group(3)
            yearOrmonth = x.group(4)[0]
            a = re.search("(\d+)-*(.+) ",over)
            overYear = a.group(2)[0]
            overYearVal = a.group(1)

            output = "{0}_{1}_TS{2}{3}B_VS_{4}{5}B".format(country,field,yearOrmonthVal,yearOrmonth,overYearVal,overYear)
           
            return output
        elif "Overnight" in input_name and "Treasury Spread" in input_name:
            x = re.search("Of (.+)_(.+) Overnight", input_name)
            field = x.group(1)[0]
            country = getCountryAbbr(x.group(2))
            a = re.search("(\d+)-*(.+) ",over)
            overYear = a.group(2)[0]
            overYearVal = a.group(1)

            output = "{0}_{1}_TSOVB_VS_{2}{3}B".format(country,field,overYearVal,overYear)
            return output
        elif "Overnight" in input_name and "Treasury Spread" not in input_name:
            x = re.search("(.+)_(.+) Overnight", input_name)
            field = x.group(1)[0]
            country = getCountryAbbr(x.group(2))

            output = "{0}_{1}_TYOVB".format(country,field)
            return output
        else:
            x = re.search("(.+)_(.+) (\d+)-*(.+)", input_name)
            field = x.group(1)[0]
            country = getCountryAbbr(x.group(2))
            yearOrmonthVal = x.group(3)
            yearOrmonth = x.group(4)[0]
            output = "{0}_{1}_TY{2}{3}B".format(country,field,yearOrmonthVal,yearOrmonth)
            return output


def globalRename(df1,df2):
  short_dataDic = []
  short_dataDictx = []
  over = df1.columns[1]
  renamed = []
  renamex = []
  for i in df2.columns[1:]:
    ans = renameCountry(i,over)
    short_dataDic.append([i,ans])
    renamed.append(ans)
  for i in df1.columns[1:]:
    ans = renameCountry(i,over)
    renamex.append(ans)
    short_dataDictx.append([i,ans])
  
  renamed.insert(0,"Date")
  renamex.insert(0,"Date")
  
  copy_df1 = df1.copy(deep=True)
  copy_df2 = df2.copy(deep=True)

  copy_df1.columns = renamex
  copy_df2.columns = renamed
  return copy_df1,copy_df2

def globalRename_withoutIndex(df1,df2):
  short_dataDic = []
  short_dataDictx = []
  over = df1.columns[0]
  renamed = []
  renamex = []
  for i in df2.columns[0:]:
    ans = renameCountry(i,over)
    short_dataDic.append([i,ans])
    renamed.append(ans)
  for i in df1.columns[0:]:
    ans = renameCountry(i,over)
    renamex.append(ans)
    short_dataDictx.append([i,ans])
  
  
  copy_df1 = df1.copy(deep=True)
  copy_df2 = df2.copy(deep=True)

  copy_df1.columns = renamex
  copy_df2.columns = renamed
  return copy_df1,copy_df2




def sortByDate(result):
  result = result.reset_index()
  result['Date'] =pd.to_datetime(result.Date)
  sorted_df = result.sort_values(by='Date',axis=0,ascending=False)
  sorted_df["Date"]=sorted_df.Date.dt.strftime('%b %d, %y')
  return sorted_df


#Fucntion to create TreasurySpreads for every country



countries =['Argentina', 'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Belgium', 'Botswana', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'China', 'Colombia', 'Croatia', 
'Cyprus', 'Czech', 'Egypt', 'France', 'Germany', 'Greece', 'Hong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kenya',
 'Malaysia', 'Malta', 'Mauritius', 'Mexico', 'Morocco', 'Namibia', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar',
  'Romania', 'Russia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'Uganda', 'Ukraine',
   'United Kingdom', 'United States', 'Vietnam']

shortlisted_countries = ["Argentina",'United Kingdom', 'United States',"Japan","China","Canada","France","Germany","Singapore","Hong","South Korea", "Australia" ]
#comment Argentina

#C-G


dd = {}
for name in countries:
    tempCont = []
    for country in countryNames:
        if name in country:
            tempCont.append(country)
            
    dd[name] = tempCont




sorted(dd.items(), key=lambda x: x[0], reverse=False)



os.chdir(main_path)
os.chdir(output_path)
doneBCont = glob.glob('*.{}'.format(xlsx_extension))
doneBCont = [i.replace(".xlsx","") for i in doneBCont]


os.chdir(main_path)
os.chdir(input_path_treasury)

#------------

# a func for  start

# a func for renaming and creating a copy 
# Will do later on 
#-------------------------------------



#-------------

counter = 0
for key in dd:
  
  # Uncomment
  # if key in doneBCont:
  #   continue

  #Testing
  if key != "China":
    continue
  # counter+=1
  # if counter >= len(countryNames)/8:
  #   break
  
  

  dd[key].sort(key=natural_keys)


  print("Working for {0} bonds".format(key))
  print("All Directories\n", dd[key])
  
  leng = len(dd[key])//2
  count = 0
  nbonds=[]
  c = 1
  prev = numpy.array([])
  for i in range(0,leng):
    print(os.getcwd())
    print(dd[key][count])
    print(dd[key][count+1],"loop")
    os.chdir(main_path)
    os.chdir(input_path_treasury)
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
  
  

  bonds = []
  for i in range(0,len(nbonds)):

    nbonds[i] = nbonds[i].set_index("Date")
    nbonds[i] = nbonds[i].apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',','')))
    bonds.append(nbonds[i])

  print(len(bonds))
  

  
  # print(bonds)
  print("-------------------------------------------\n------------------------")
 
  newBonds = []

  for i in range(0,len(bonds)):
    if i == 0:
      continue
    else:
      #Logic 1 >> Harder
      # x = bonds[i].sub(bonds[0],fill_value=0)
      # x = x[~x.index.duplicated()]

      # xl = x.add(bonds[0],fill_value=0)
      # xl = xl[~xl.index.duplicated()]

      # mdxl = xl.replace(0.0, numpy.nan)
      # mdxl = mdxl[~mdxl.index.duplicated()]

      # yl = bonds[i].sub(x,fill_value=0)
      # yl = yl[~yl.index.duplicated()]

      # xfl = mdxl.sub(yl,fill_value=numpy.nan)
      # xfl = xfl[~xfl.index.duplicated()]

      # newBonds.append(xfl)

      #Logic 2 >> 
      xf = bonds[i].sub(bonds[0])
      xf = xf[~xf.index.duplicated()]
      xf = xf.fillna(value="na")
      # print(xf)
      

      newBonds.append(xf)

  #Extras
  # print(newBonds)

  # y = pd.merge(newBonds[0],newBonds[1],on=["Date"] , how="outer")
  # y = y[~y.index.duplicated()]
  # print(y)
  # exit()


  #Trick 1
  #Fill na before merge
  
  # pd.set_option('display.max_columns', None)
  
    
  bonds = []

  bonds = newBonds.copy()

  print(len(bonds))
   


  #--------------------------------------------------

  
  


  c=0
  for x in range(0,len(bonds)):
        if x == 0:

          bonds[x] = bonds[x].rename(columns={'Price':'Treasury Spread Of Price_{0}'.format(dd[key][x+3]),
            'Change %':'Treasury Spread Of Change %_{0}'.format(dd[key][x+3]),'High':'Treasury Spread Of High_{0}'.format(dd[key][x+3]),
            'Low':'Treasury Spread Of Low_{0}'.format(dd[key][x+3]),'Open':'Treasury Spread Of Open_{0}'.format(dd[key][x+3])
                                })
          c = x+3
        else:
          new = c+2
          bonds[x] = bonds[x].rename(columns={'Price':'Treasury Spread Of Price_{0}'.format(dd[key][new]),
            'Change %':'Treasury Spread Of Change %_{0}'.format(dd[key][new]),'High':'Treasury Spread Of High_{0}'.format(dd[key][new]),
            'Low':'Treasury Spread Of Low_{0}'.format(dd[key][new]),'Open':'Treasury Spread Of Open_{0}'.format(dd[key][new])
                                })
          c = new


 

  



 
  if len(bonds) == 2:
    # result = pd.DataFrame.drop_duplicates(pd.merge(bonds[0],bonds[1],on=["Date"] , how="outer"))
    # result = result.fillna(value="na")

    result = pd.merge(bonds[0],bonds[1],on=["Date"] , how="outer")
    result = result[~result.index.duplicated()]
    result = result.fillna(value="na")
    
    
    
    
  elif len(nbonds) == 1:
    result = nbonds[0]
  else:
    
    result = ''
    for i in range(0,len(bonds)):  #for i in range(0,len(bonds),2):
      
      if i == 0:
        # result = pd.DataFrame.drop_duplicates(pd.merge(bonds[i],bonds[i+1],on=["Date"] , how="outer"))
        # result = result.fillna(value="na")
        result = pd.merge(bonds[i],bonds[i+1],on=["Date"] , how="outer")
        result = result[~result.index.duplicated()]
        result = result.fillna(value="na")
      elif i == 1:
        continue
      else:
        
        # result = pd.DataFrame.drop_duplicates(pd.merge(result,bonds[i], on=["Date"] , how="outer"))
        # result = result.fillna(value="na")
        result = pd.merge(result,bonds[i], on=["Date"] , how="outer")
        result = result[~result.index.duplicated()]
        result = result.fillna(value="na")

  
  print(result)
  # exit()
        

  

  

  
 
  


  #----------------------
  bonxs = [i for i in nbonds]


  
  
  
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
    # resulx = pd.DataFrame.drop_duplicates(pd.merge(bonxs[0],bonxs[1],on=["Date"] , how="outer"))
    resulx = pd.merge(bonxs[0],bonxs[1],on=["Date"] , how="outer")
    resulx = resulx[~resulx.index.duplicated()]
    
    
    
    
  elif len(bonxs) == 1:
    resulx = bonxs[0]
  else:
    
    resulx = ''
    for i in range(0,len(bonxs)):
      
      if i == 0:
        #resulx = pd.DataFrame.drop_duplicates(pd.merge(bonxs[i],bonxs[i+1],on=["Date"] , how="outer"))
        resulx = pd.merge(bonxs[i],bonxs[i+1],on=["Date"] , how="outer")
        resulx = resulx[~resulx.index.duplicated()]
        
        
   
        
      elif i == 1:
        continue
      else:
        
        
        # resulx = pd.DataFrame.drop_duplicates(pd.merge(resulx,bonxs[i], on=["Date"] , how="outer"))
        resulx = pd.merge(resulx,bonxs[i], on=["Date"] , how="outer")
        resulx = resulx[~resulx.index.duplicated()]
        
    
  #pd.set_option('display.max_columns', None)
  
  b = resulx.columns[:]
  
  resulx[b] =  resulx[b].fillna(value="na")

  
  
        
        
  
  
      

        
  
  

#--------------------------------

  #print([pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"]).set_index("Date", inplace = True) for i in bonds])
 
  print("Merged")

  
  
  
  # try:
  #   result = pd.DataFrame.drop_duplicates(result)
  # except:
  #   pass




  #----------------------------------- Shortlisted -----------------------------------------------------
  #sorted =spread, sortex=yeild
  #if key is defferent don't create Shortlisted
  print("Creating Shortlisted Ouput")
  #Uncomment CHANGE "!, not"
  if key not in shortlisted_countries:

    #------------For Yeild
    x = resulx.columns[0:-1:5]
    xy = list(x)
    mod_resulx = resulx[xy]
    shortlist_sortex_df = sortByDate(mod_resulx)
    shortlist_sortex_df.columns = shortlist_sortex_df.columns.str.replace('.csv', '')
    #print(shortlist_sortex_df, "chcek")
    #Almost done


    #---------For Spread
    x = result.columns[0:-1:5]
    xy = list(x)
    mod_result = result[xy]
   
    neg_mod_result = mod_result.replace("na",0)
    neg_mod_result = neg_mod_result.mask(neg_mod_result >= 0, 0)
    neg_mod_result = neg_mod_result.mask(neg_mod_result < 0, 1)
    #Renaming Column  Name
    neg_mod_result=neg_mod_result.add_prefix("Incidences Of Negative ")
    
    final_mod_result = pd.concat([mod_result, neg_mod_result], axis=1)

    shortlist_sorted_df = sortByDate(final_mod_result)
    shortlist_sorted_df.columns = shortlist_sorted_df.columns.str.replace('.csv', '')
    print(shortlist_sorted_df)

    #------------------------------------Renaming Starts For Shorlisted---------------------
    copy_shortlist_sortex_df,copy_shortlist_sorted_df = globalRename(shortlist_sortex_df,shortlist_sorted_df)
    print(copy_shortlist_sorted_df)

    #-----------------------Renaming Ends For Shortlisted---------------------


    #----------- Writing Files -----------
    print("Writing Shortlisted File")

    os.chdir(main_path)
    os.chdir(shortlist_output_path)
    writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
    shortlist_sortex_df.to_excel(writer,'Merging By Date',index=False)
    shortlist_sorted_df.to_excel(writer,'Treasury Spread',index=False)
    writer.save()

    os.chdir(main_path)
    os.chdir(shortlist_production_ouput_path)
    #Uncomment
    # writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
    # copy_shortlist_sortex_df.to_excel(writer,'Merging By Date',index=False)
    # copy_shortlist_sorted_df.to_excel(writer,'Treasury Spread',index=False)
    # writer.save()
    os.chdir(main_path)
    #-------------------
    



  
    print("Done Shortlisting {0}".format(key))
  #Get the price column only

  #create folder and write to csv here
  # ----------------------------------------------------------------------------------------------------------

  # ------------------------Quaterly Insights-----------------------
  
  #Uncomment
  if key in shortlisted_countries:

    print("Working for Quaterly Insights")
    #------------For Yeilds-----
    #-------------Logic 1 --------
    # x = resulx.columns[0:-1:5]
    # xy = list(x)
    # price_resulx = resulx[xy]
    # price_resulx.columns =  price_resulx.columns.str.replace('.csv', '')
    # price_resulx = price_resulx.replace("na",numpy.nan)

    # get_last = lambda x: x.fillna(method='ffill').iloc[-1]
    # get_negatives = lambda x: sum(x<0)   #lambda x: sum(x)>0
    # get_last.__name__ = "Ending Yeild Each Quarter"
    # agg_resulx_avg = price_resulx.agg(['mean',get_last ])
    # agg_resulx_avg = agg_resulx_avg.rename(index={"mean": 'Average Yeild Each Quarter'})
    # print(agg_resulx_avg)


    # #-------------For Spread----------
    # x = result.columns[0:-1:5]
    # xy = list(x)
    # price_result = result[xy]
    # price_result.columns =  price_result.columns.str.replace('.csv', '')
    # price_result = price_result.replace("na",numpy.nan)
    # get_negatives.__name__ = "No Of Negative Spread Each Quarter"
    # get_last.__name__ = "Ending Spread Each Quarter"
    # agg_result_avg = price_result.agg(['mean',get_last,"min",get_negatives ])
    # agg_result_avg = agg_result_avg.rename(index={"mean": 'Average Spread Each Quarter'})
    # agg_result_avg = agg_result_avg.rename(index={"min": 'Minimum Spread Each Quarter'})

    #---------------Logic 2----------------------
    
    #-----------------For Yields------------------
    x = resulx.columns[0:-1:5]
    xy = list(x)
    price_resulx = resulx[xy]
    price_resulx.columns =  price_resulx.columns.str.replace('.csv', '')
    price_resulx = price_resulx.replace("na",numpy.nan)
    
    date_resulx = price_resulx.reset_index()
    date_resulx['Date'] =pd.to_datetime(date_resulx.Date)
    date_sortex_df = date_resulx.sort_values(by='Date',axis=0,ascending=False)
    date_sortex_df = date_sortex_df.set_index("Date")
    # sorted_df["Date"]=sorted_df.Date.dt.strftime('%b %d, %y')
    # return sorted_df
    
    # get_last = lambda x: x.fillna(method='ffill').iloc[-1]
    #TEST
    def get_negatives(x):
      if sum(x<0)==0 and sum(x>0)==0:
        return "nan" 
      else:
        return sum(x<0)
    #
    # get_negatives = lambda x: numpy.nan if(x.empty()) else sum(x<0)
    get_negatives.__name__ = "Number Of Negative Incidences"
    # get_last2 = lambda x: x.notna()[::-1].idxmax()
    # get_last.__name__ = "Ending Yeild Each Quarter"
    # date_sortex_df = date_sortex_df.resample("QS").fillna(method='ffill')
    date_sortex_df = date_sortex_df.resample("QS").agg(['mean',"last"]) #drop na = True
    # date_sortex_df = date_sortex_df.rename(index={"mean": 'Average Yeild Each Quarter'})
    

    # date_sortex_df.rename(columns = {'mean':'Average Yeild', 'min':'Minimum Yeild', "Price_Argentina 1-Year Bond Yield Historical Data":"non:"
    #                             }, inplace = True)



    #-------------------For Spread----------------
    x = result.columns[0:-1:5]
    xy = list(x)
    price_result = result[xy]
    price_result.columns =  price_result.columns.str.replace('.csv', '')
    price_result = price_result.replace("na",numpy.nan)

    date_result = price_result.reset_index()
    date_result['Date'] =pd.to_datetime(date_result.Date)
    date_sorted_df = date_result.sort_values(by='Date',axis=0,ascending=False)
    date_sorted_df = date_sorted_df.set_index("Date")


    date_sorted_df = date_sorted_df.resample("QS").agg(['mean',"last",get_negatives,"min"]) #drop na = True




    #COLUMN RENAMING
    
    a, b= globalRename_withoutIndex(price_resulx,price_result)
    

    #GETTING COLUMN NAMES Yeilds
    col_names_a=[]
    col_names_b = []

    a = list(a)
    co = 0
    for i in range(0,len(a)*2,2):
      renam = "Average_TY_"+a[int(co)]
      renam2 = "End_Of_Quarter_TY_"+a[int(co)]
      col_names_a.append(renam)
      col_names_a.append(renam2)
      co+=1

    b = list(b)
    co =0
    for i in range(0,len(b)):
      renam = "Average_SPD_"+b[i]
      renam2 = "End_Of_Quarter_SPD_"+b[i]
      renam3 = "No_Of_Negative_SPD_"+b[i]
      renam4 = "Min_SPD_"+b[i]
      col_names_b.append(renam)
      col_names_b.append(renam2)
      col_names_b.append(renam3)
      col_names_b.append(renam4)
    # print(col_names_b)
    #ABOVE two for loops can be simplified into one


    date_sortex_df.columns = col_names_a
    date_sorted_df.columns = col_names_b
    
    #------------- Fill Na and Set Date
    
    mod_date_sortex_df = date_sortex_df.fillna("na")
    mod_date_sortex_df = mod_date_sortex_df.reset_index()
    mod_date_sortex_df["Date"]=mod_date_sortex_df.Date.dt.strftime('%b %d, %y')


    print(mod_date_sortex_df)

    mod_date_sorted_df = date_sorted_df.fillna("na")
    mod_date_sorted_df = mod_date_sorted_df.reset_index()
    mod_date_sorted_df["Date"]=mod_date_sorted_df.Date.dt.strftime('%b %d, %y')


    print(mod_date_sorted_df)
    
    
    

    #Research on aggregiation
    #https://stackoverflow.com/questions/53461722/pandas-how-to-get-count-of-negative-and-positive-values-in-a-row

    #------------------Writing To File-----------
    

    # mod_date_sortex_df = StyleFrame(mod_date_sortex_df, Styler(shrink_to_fit=False, wrap_text=False))
    # print(mod_date_sortex_df)

    #---------Imputed
    

    # threshed = len(date_sorted_df.columns) - 1
    # threshex = len(date_sortex_df.columns) - 1
    # print(threshex,threshed)

    # drop_mod_date_sortex_df = mod_date_sortex_df.replace("na",numpy.nan).dropna(how="all",thresh=3).fillna("na")
    # drop_mod_date_sorted_df = mod_date_sorted_df.replace("na",numpy.nan).dropna(thresh=4).fillna("na")
    # print(drop_mod_date_sorted_df)


    print(mod_date_sortex_df)
    train = mod_date_sortex_df.replace("na",numpy.nan)

    #ALGO 1
    #Part 1
    print(train.isnull().any())
    null_columns = train.columns[train.isnull().any()]
    v = train[null_columns]
    print(train,"Train")

    # print(train.Average_TY_AR_P_TY1YB.shift())


    # xy = train.columns[1:-1:2]
    # drop_xy = list(xy)[1:]
    # avg_train = train[list(xy)]
    # drop_avg_train = train[drop_xy]
    # print(drop_avg_train)
    # exit()

    #MAIN FORMULA
    #train['Final Rate'] = train['Average_TY_AR_P_TY2YB'].fillna(train['Average_TY_AR_P_TY2YB'].ffill() - train.Average_TY_AR_P_TY1YB)
    #MAIN FORMULA

    #avg_train = avg_train.fillna(avg_train.ffill() - avg_train.Average_TY_AR_P_TY1YB)
    # drop_avg_train.apply(lambda x: print(x.fillna(x.ffill() - avg_train.Average_TY_AR_P_TY1YB)),axis=1)


    #new_train= drop_avg_train.apply(lambda x: x.fillna(x.ffill() - train.Average_TY_AR_P_TY1YB))
    yx = train.columns[3:-1]
    new_train = train[list(yx)]
    new_train= new_train.apply(lambda x: x.fillna(x.ffill() - train.iloc[:,1])) #Uncomment Make it Not Hardcoded

    # new_train= new_train.apply(lambda x: x.fillna(x.ffill() - train.Average_TY_AR_P_TY1YB))

    ab = train.columns[0:3]
    add_train =  train[list(ab)]
    
    final_train = pd.merge(add_train,new_train,left_index=True,right_index=True)



    #########FOR SPREADS

    spreads_train = mod_date_sorted_df.replace("na",numpy.nan)
    print(spreads_train,"spread_train")

    yx = spreads_train.columns[5:]
    new_spread_train = spreads_train[list(yx)]
    print(new_spread_train)
    

    yx =  new_spread_train.columns[0::4]
    xy =  new_spread_train.columns[1::4]
    # avg = new_spread_train[list(yx)]
    # end = new_spread_train[list(yx)]
    avg_end = new_spread_train[list(yx)+list(xy)]
    print(avg_end)



    yx =  new_spread_train.columns[2::4]
    xy =  new_spread_train.columns[3::4]
    min_neg_cols = list(xy)+list(yx)
    min_neg = new_spread_train[list(xy)+list(yx)]
    print(min_neg)
    
    
    new_avg_end= avg_end.apply(lambda x: x.fillna(x.ffill() - spreads_train.iloc[:,1]))  #UNCOMMENT MAKe it un hardcoded


    ab = spreads_train.columns[0:5]
    add_spread =  spreads_train[list(ab)]

    # ab = train.columns[0:3]
    # add_train =  train[list(ab)]
    
    merge_spred = pd.merge(new_avg_end,min_neg,left_index=True,right_index=True)
    print(merge_spred)


    x = len(merge_spred.columns)/4
    print(x)

    ab = []
    for i in range(int(x)):
      ab.append(list(merge_spred.columns[i::int(x)]))
    
    flatList = [ item for elem in ab for item in elem]
    print(flatList)
    
    new_merge_spread = merge_spred[flatList]
    pd.set_option('display.max_rows', None)

    print(new_merge_spread)

    filled_spreadd = new_merge_spread.fillna(axis=1,limit=1,method="ffill")
    filled_spread=filled_spreadd.replace("nan",numpy.nan)
    


    def fillneg(x):
      val  = x.ffill()
      if val > 0:
        return x.fillna(0)
      else:
        return x.fillna(1)
    # x.fillna(x.ffill() - spreads_train.iloc[:,1]
    #filled_spread= filled_spread.apply(lambda x: x.fillna(x.ffill(axis=1)- x.ffill(axis=1) ) )
    #new_avg_end= avg_end.apply(lambda x: x.fillna(x.ffill() - spreads_train.iloc[:,1]))  #UNCOMMENT MAKe it un hardcoded

    # df['c'] = df.apply(
    #     lambda row: row['a']*row['b'] if np.isnan(row['c']) else row['c'],
    #     axis=1
    # )

    def fillneg2(row):
      #if numpy.isnan(row):
      # y = row.ffill()
      # print(y)
      if row.End_Of_Quarter_SPD_CN_P_TS3YB_VS_1YB > 0:
        return 0 #4
      elif row.End_Of_Quarter_SPD_CN_P_TS3YB_VS_1YB < 0:
        return 1 #2
      else:
        return row
        # if row.ffill() > 0:
        #  return 0
        # else:
        #   return 1
      # else:
      #   return row
    filled_spread = filled_spread.apply(
        lambda x: x.fillna(fillneg2(x)),
        axis=1,
        
    )
    #WORKING HERE

    #filled_spread = filled_spread.fillna(axis=1,limit=1,method=fillneg)


    
    print(filled_spread)
    # final_spread = pd.merge(add_spread,new_avg_end,left_index=True,right_index=True)

    filled_spread = pd.merge(add_spread,filled_spread,left_index=True,right_index=True)


    # exit()

    filled_spread = filled_spread.fillna("na")
    final_train = final_train.fillna("na")
    # print(final_spread)
    os.chdir(main_path)
    os.chdir(imputed_quarterly_path)
    writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
    final_train.to_excel(writer,'Merging By Date',index=False)
    filled_spread.to_excel(writer,'Treasury Spread',index=False)
    writer.save()
    os.chdir(main_path)


    # print(final_train)
    exit()

    #ALGO 0
    # drop_mod_date_sortex_df = mod_date_sortex_df.replace("na",numpy.nan).fillna(method='ffill').fillna("na")
    # drop_mod_date_sorted_df = mod_date_sorted_df.replace("na",numpy.nan).fillna(method='ffill').fillna("na")
    # print(drop_mod_date_sortex_df)
    # print(mod_date_sortex_df)
    #-----------------

    

    # os.chdir(main_path)
    # os.chdir(imputed_quarterly_path)
    # writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
    # drop_mod_date_sortex_df.to_excel(writer,'Merging By Date',index=False)
    # drop_mod_date_sorted_df.to_excel(writer,'Treasury Spread',index=False)
    # writer.save()
    # os.chdir(main_path)

    exit()



    #----------------
    print("Writing Quarterly Insights")
    os.chdir(main_path)
    os.chdir(quarterly_path)

    writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
    mod_date_sortex_df.to_excel(writer,'Merging By Date',index=False)
    mod_date_sorted_df.to_excel(writer,'Treasury Spread',index=False)
    writer.save()
    os.chdir(main_path)

    print("Done Quarterly Insights For",key)



  #--------------------
  #Imputed Quarterly Insights
  # if key in shortlisted_countries:


  #exit()
  # -----------------------------------------------
  
  

  x = result.columns[0:-1:5]
  y = result.columns[1:-1:5]
  z = result.columns[2:-1:5]
  a = result.columns[3:-1:5]
  b = result.columns[4::5]
  
  xy = list(x)+list(y)+list(z)+list(a)+list(b)
  
  result = result[xy]
  print("Changed till here")

#---------------------

  x = resulx.columns[0:-1:5]
  y = resulx.columns[1:-1:5]
  z = resulx.columns[2:-1:5]
  a = resulx.columns[3:-1:5]
  b = resulx.columns[4::5]
  
  xy = list(x)+list(y)+list(z)+list(a)+list(b)
  
  resulx = resulx[xy]


 
  
  # result = result.reset_index()
  # result['Date'] =pd.to_datetime(result.Date)
  # sorted_df = result.sort_values(by='Date',axis=0,ascending=False)
  # sorted_df["Date"]=sorted_df.Date.dt.strftime('%b %d, %y')
  sorted_df = sortByDate(result)

  
  
  

  print(sorted_df,"...")
  



  #--------------------
  # resulx = resulx.reset_index()
  # resulx['Date'] =pd.to_datetime(resulx.Date)
  # sortex_df = resulx.sort_values(by='Date',axis=0,ascending=False)
  # sortex_df["Date"]=sortex_df.Date.dt.strftime('%b %d, %y')

  sortex_df = sortByDate(resulx)



  os.chdir(main_path)
  print(main_path)


  os.chdir(output_path)

  print(sortex_df,"...")

  print("Sorted By Date")

  #--------------




  
  sortex_df.columns = sortex_df.columns.str.replace('.csv', '')
  sorted_df.columns = sorted_df.columns.str.replace('.csv', '')

  print("Replaced String")


  
  dataDictd = []
  dataDictx = []

 
  #------------------------------------Renaming Starts---------------------
  copy_sortex_df,copy_sorted_df = globalRename(sortex_df,sorted_df)

  # over = sortex_df.columns[1]
  # renamed = []
  # renamex = []
  # for i in sorted_df.columns[1:]:
  #   ans = renameCountry(i,over)
  #   dataDictd.append([i,ans])
  #   renamed.append(ans)
  # for i in sortex_df.columns[1:]:
  #   ans = renameCountry(i,over)
  #   renamex.append(ans)
  #   dataDictx.append([i,ans])
  
  # renamed.insert(0,"Date")
  # renamex.insert(0,"Date")
  
  # copy_sortex_df = sortex_df.copy(deep=True)
  # copy_sorted_df = sorted_df.copy(deep=True)

  # copy_sorted_df.columns = renamed
  # copy_sortex_df.columns = renamex

  #-----------------------Renaming Ends---------------------



  sortex_df = StyleFrame(sortex_df, Styler(shrink_to_fit=False, wrap_text=False))
  sortex_df.set_column_width(sortex_df.columns,12) 
  writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))

  sorted_df = StyleFrame(sorted_df, Styler(shrink_to_fit=False, wrap_text=False))
  sorted_df.set_column_width(sorted_df.columns,12) 

  print("Stylesheet Created")

  sortex_df.to_excel(writer,'Merging By Date',index=False)
  sorted_df.to_excel(writer,'Treasury Spread',index=False)
 
  writer.save()




  os.chdir(main_path)
  os.chdir(production_ouput_path)
  writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
  copy_sortex_df.to_excel(writer,'Merging By Date',index=False)
  copy_sorted_df.to_excel(writer,'Treasury Spread',index=False)
  writer.save()

  writeToCsv(dataDictd,"dataDictTreasurySpreads.csv")
  writeToCsv(dataDictx, "dataDictTreasuryYields.csv")






  os.chdir(main_path)






# print(dataDictd)
# print(dataDictx)






exit()


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

#Output, Production Output Checked
#Shortlisted , Prod Shortlisted Correct
#Try countries with space in name, or ajeeb sa name

#Checked except quarterly insights
#Uncomment vefore sharing script , go through




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
dataDictd = []
dataDictx = []

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
createADic()


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
        # print(input_name,"------")   
        if "Treasury Spread" in input_name and "Overnight" not in input_name:

            # print(input_name,"---------")
            x = re.search("Of (.+)_(.+) (\d+)-*(.+) Over", input_name)
            # print(x.group(1)[0],"..............")
            field = x.group(1)[0]
            country = getCountryAbbr(x.group(2))
            yearOrmonthVal = x.group(3)
            yearOrmonth = x.group(4)[0]
            a = re.search("(\d+)-*(.+) ",over)
            overYear = a.group(2)[0]
            overYearVal = a.group(1)

            

            output = "{0}_{1}_TS{2}{3}B_VS_{4}{5}B".format(country,field,yearOrmonthVal,yearOrmonth,overYearVal,overYear)
            #SAMPLE OUTPUT Unknown code_P_TS1YB_VS_1YB
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


def globalRename(df1,df2,inc):
  global dataDictd
  global dataDictx

  over = df1.columns[1+inc]
  renamed = []
  renamex = []
  for i in df2.columns[1:]:
    ans = renameCountry(i,over)
    dataDictd.append([i,ans])
    renamed.append(ans)
  for i in df1.columns[1:]:
    ans = renameCountry(i,over)
    renamex.append(ans)
    dataDictx.append([i,ans])
  
  renamed.insert(0,"Date")
  renamex.insert(0,"Date")
  
  copy_df1 = df1.copy(deep=True)
  copy_df2 = df2.copy(deep=True)

  copy_df1.columns = renamex
  copy_df2.columns = renamed
  return copy_df1,copy_df2

def globalRename_withoutIndex(df1,df2,inc):
  short_dataDic = []
  short_dataDictx = []
  # print(df1)
  # print(df2)
  over = df1.columns[0+inc]
  # print(over, inc)
  # exit()
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








#---------------Fucntions Inside
def extractingTreasurySpreads(bonds,inc):
  
  c=0
  print(len(bonds))
  for x in range(0,len(bonds)):
        if x == 0:
          currNum = dd[key][x+(3+inc)]
          againstNum = dd[key][(x+(3+inc)-2)].split(" ")[-5]
          bonds[x] = bonds[x].rename(columns={'Price':'Treasury Spread Of Price_{0} Over {1} Bond Yeild'.format(currNum,againstNum),
            'Change %':'Treasury Spread Of Change %_{0} Over {1} Bond Yeild'.format( currNum,againstNum),
            'High':'Treasury Spread Of High_{0} Over {1} Bond Yeild'.format(currNum,againstNum),
            'Low':'Treasury Spread Of Low_{0} Over {1} Bond Yeild'.format(currNum,againstNum),
            'Open':'Treasury Spread Of Open_{0} Over {1} Bond Yeild'.format(currNum,againstNum)
                                })
          c = x+(3+inc)
        else:
          new = c+2
          agains = dd[key][inc+1].split(" ")[-5]

          #agains = dd[key][new-2].split(" ")[-5]

          # new = c+(2+inc)
          #agains = dd[key][c-2].split(" ")[-5]
          # agains = dd[key][inc+2].split(" ")[-5]
          # print(c, key)
          print(new)
          print(agains)
          # print(dd[key][new], "against", dd[key][inc+1])
          #exit()
          bonds[x] = bonds[x].rename(columns={'Price':'Treasury Spread Of Price_{0} Over {1} Bond Yeild'.format(dd[key][new],agains),
            'Change %':'Treasury Spread Of Change %_{0} Over {1} Bond Yeild'.format(dd[key][new], agains),
            'High':'Treasury Spread Of High_{0} Over {1} Bond Yeild'.format(dd[key][new],agains),
            'Low':'Treasury Spread Of Low_{0} Over {1} Bond Yeild'.format(dd[key][new],agains),
            'Open':'Treasury Spread Of Open_{0} Over {1} Bond Yeild'.format(dd[key][new],agains)
                                })
          c = new

  
  
  

  if len(bonds) == 2:
    result = pd.merge(bonds[0],bonds[1],on=["Date"] , how="outer")
    result = result[~result.index.duplicated()]
    result = result.fillna(value="na")
    
  elif len(bonds) == 1:
    result = bonds[0]
  else:
    
    result = ''
    for i in range(0,len(bonds)):  #for i in range(0,len(bonds),2):
      
      if i == 0:
        result = pd.merge(bonds[i],bonds[i+1],on=["Date"] , how="outer")
        result = result[~result.index.duplicated()]
        result = result.fillna(value="na")
      elif i == 1:
        continue
      else:
        result = pd.merge(result,bonds[i], on=["Date"] , how="outer")
        result = result[~result.index.duplicated()]
        result = result.fillna(value="na")
  
  #Rearranging Columns
  x = result.columns[0:-1:5]
  y = result.columns[1:-1:5]
  z = result.columns[2:-1:5]
  a = result.columns[3:-1:5]
  b = result.columns[4::5]
  
  xy = list(x)+list(y)+list(z)+list(a)+list(b)
  result = result[xy]


  #Sorting Columns By Date
  sorted_df = sortByDate(result)
  print(sorted_df,"...............................................")

 
  sorted_df.columns = sorted_df.columns.str.replace('.csv', '')

  return result,sorted_df

def extractingTreasuryYeilds(nbonds):
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
        resulx = pd.merge(bonxs[i],bonxs[i+1],on=["Date"] , how="outer")
        resulx = resulx[~resulx.index.duplicated()]
      elif i == 1:
        continue
      else:        
        resulx = pd.merge(resulx,bonxs[i], on=["Date"] , how="outer")
        resulx = resulx[~resulx.index.duplicated()]
  
  b = resulx.columns[:]
  
  resulx[b] =  resulx[b].fillna(value="na")

  x = resulx.columns[0:-1:5]
  y = resulx.columns[1:-1:5]
  z = resulx.columns[2:-1:5]
  a = resulx.columns[3:-1:5]
  b = resulx.columns[4::5]
  
  xy = list(x)+list(y)+list(z)+list(a)+list(b)
  
  resulx = resulx[xy]
  sortex_df = sortByDate(resulx)

  
  sortex_df.columns = sortex_df.columns.str.replace('.csv', '')

  return resulx,sortex_df


def shortlistedYeild(resulx):
    y = len(list(resulx.columns))/5
    x = resulx.columns[0:int(y)]
    xy = list(x)
    mod_resulx = resulx[xy]
    shortlist_sortex_df = sortByDate(mod_resulx)
    shortlist_sortex_df.columns = shortlist_sortex_df.columns.str.replace('.csv', '')
    #print(shortlist_sortex_df, "chcek")
    #Almost done
    return shortlist_sortex_df

def shortlistedSpread(result):

    #---------For Spread
    # x = result.columns[0:-1:5]
    y = len(list(result.columns))/5
    x = result.columns[0:int(y)]
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
    return shortlist_sorted_df


#UNCOMMENT
#Working here! Problems....
def quarterlyInsightsYeild(resulx , tempdf2, inc):
    # x = resulx.columns[0:-1:5]
    y = len(list(resulx.columns))/5
    x = resulx.columns[0:int(y)]
    # print(resulx.columns)
    # exit()
    xy = list(x)
    price_resulx = resulx[xy]
    price_resulx.columns =  price_resulx.columns.str.replace('.csv', '')
    price_resulx = price_resulx.replace("na",numpy.nan)
    
    date_resulx = price_resulx.reset_index()
    date_resulx['Date'] =pd.to_datetime(date_resulx.Date)
    date_sortex_df = date_resulx.sort_values(by='Date',axis=0,ascending=False)
    date_sortex_df = date_sortex_df.set_index("Date")

    

    get_negatives.__name__ = "Number Of Negative Incidences"
    date_sortex_df = date_sortex_df.resample("QS").agg(['mean',"last"]) #drop na = True

    
    print(price_resulx,"000000000000000000")
    a, b= globalRename_withoutIndex(price_resulx,tempdf2, inc)
    

    #GETTING COLUMN NAMES Yeilds
    col_names_a=[]

    a = list(a)
    co = 0
    for i in range(0,len(a)*2,2):
      renam = "Average_TY_"+a[int(co)]
      renam2 = "End_Of_Quarter_TY_"+a[int(co)]
      col_names_a.append(renam)
      col_names_a.append(renam2)
      co+=1




    date_sortex_df.columns = col_names_a
    
    #------------- Fill Na and Set Date
    
    mod_date_sortex_df = date_sortex_df.fillna("na")
    mod_date_sortex_df = mod_date_sortex_df.reset_index()
    mod_date_sortex_df["Date"]=mod_date_sortex_df.Date.dt.strftime('%b %d, %y')


    print(mod_date_sortex_df)

    return mod_date_sortex_df, price_resulx, date_sortex_df



def quarterlyInsightsSpread(result,price_resulx,date_sortex_df, inc):
    y = len(list(result.columns))/5
    x = result.columns[0:int(y)]
    #x = result.columns[0:-1:5]
    # print(x)
    # exit()
    xy = list(x)
    price_result = result[xy]
    price_result.columns =  price_result.columns.str.replace('.csv', '')
    price_result = price_result.replace("na",numpy.nan)

    date_result = price_result.reset_index()
    date_result['Date'] =pd.to_datetime(date_result.Date)
    date_sorted_df = date_result.sort_values(by='Date',axis=0,ascending=False)
    date_sorted_df = date_sorted_df.set_index("Date")


    date_sorted_df = date_sorted_df.resample("QS").agg(['mean',"last",get_negatives,"min"]) #drop na = True

    print(price_resulx,"000000000000000000")
    a, b= globalRename_withoutIndex(price_resulx,price_result, inc)
    

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

    
      print()

    date_sortex_df.columns = col_names_a
    date_sorted_df.columns = col_names_b
    
    #------------- Fill Na and Set Date
    

    mod_date_sorted_df = date_sorted_df.fillna("na")
    mod_date_sorted_df = mod_date_sorted_df.reset_index()
    mod_date_sorted_df["Date"]=mod_date_sorted_df.Date.dt.strftime('%b %d, %y')


    print(mod_date_sorted_df)
    

    return mod_date_sorted_df




def ImputedYeild(mod_date_sortex_df):
    imputed_yeild_df = mod_date_sortex_df.replace("na",numpy.nan).fillna(method='ffill').fillna("na")
    return imputed_yeild_df


def ImputedSpread(imputed_yeild_df, mod_date_sorted_df,inc):
  

    ### SPREADS ####
    imput_y = imputed_yeild_df.replace('na',numpy.nan)


 

    x = imput_y.columns[1::2]
    y = imput_y.columns[2::2]

    # print(x)
    # print(y)
    # exit()

    avg = pd.DataFrame()

    # count =0
    # for i in list(x):
    #   count+=1
    #   if count == 1:
        
    #     continue
    #   else:
  
        
    #     avg["avg{0}".format(count)] = imput_y[i] - imput_y.iloc[:,1]
    # count =0
    # inc  = 1
    print(inc)
    # exit()
    count = 1
    startFrom = 1 + inc
    if inc == 0:
      cc = 1
    else: 
      cc = inc + 2
    for i in range(startFrom, len(list(x))):
      
      
      # print(imput_y[x[i]])
      # print(imput_y.iloc[:,cc])
      
      
      
      avg["avg{0}".format(count)] = imput_y[x[i]] - imput_y.iloc[:,cc]
      count +=1
    
    
    end = pd.DataFrame()
    count =1
    if inc == 0:
      cc = 2
    else: 
      cc = inc + 2
    for i in range(startFrom, len(list(y))):
      
        
      end["end{0}".format(count)] = imput_y[y[i]] - imput_y.iloc[:,cc] #mistake here
      count += 1

    avg_end = pd.merge(avg,end,left_index=True,right_index=True)
    # print(avg_end)
    # exit()

   


              #Renaming Avg End
    len_ae = len(avg_end.columns)/2
    len_ae = int(len_ae)
    z = mod_date_sorted_df.columns[1::4]
    a = mod_date_sorted_df.columns[2::4]
    
    
    naming = list(z)+list(a)

    print(avg_end)
    print(naming)
    
    avg_end.columns = naming

    spreads_train = mod_date_sorted_df.replace("na",numpy.nan)
    yx =  spreads_train.columns[3::4]
    xy =  spreads_train.columns[4::4]
    min_neg = spreads_train[list(xy)+list(yx)]
    print(min_neg)

    imp_spread = pd.merge(avg_end,min_neg,left_index=True,right_index=True)


    lst = []
    for i in range(len_ae):

      mod = imp_spread.columns[i::len_ae]
      lst += list(mod)

    print(lst)


    imp_spread = imp_spread[lst]

          #Fill NA Min
    imp_spread = imp_spread.fillna(axis=1,limit=1,method="ffill")
    imp_spread=imp_spread.replace("nan",numpy.nan) #Uncomment Check

          #NEg Jugaar
    colNames = imp_spread.columns
    listOfDFRows = imp_spread.to_numpy().tolist()
    for currCol in range(1,len(listOfDFRows)):
      for col in range(1,len(listOfDFRows[currCol])):
          if math.isnan(listOfDFRows[currCol][col]):
            if listOfDFRows[currCol][col-1] < 0:
              listOfDFRows[currCol][col] = 1
            elif listOfDFRows[currCol][col-1] > 0:
              listOfDFRows[currCol][col] = 0

    print(len(listOfDFRows))



    imputed_spread = pd.DataFrame(listOfDFRows)
    imputed_spread.columns = colNames


          #Add Date Col
    date = mod_date_sorted_df.columns[0]
    date = mod_date_sorted_df[date]
    imputed_spread.insert(0, "Date", date)

    print(imputed_spread)

        #Writing


    final_spread_imputed_quartely = mod_date_sorted_df.copy(deep=True)
    final_spread_imputed_quartely = final_spread_imputed_quartely.replace("na",numpy.nan).replace("nan",numpy.nan)
    final_spread_imputed_quartely=final_spread_imputed_quartely.fillna(imputed_spread)
    final_spread_imputed_quartely = final_spread_imputed_quartely.fillna("na")

    
    print(final_spread_imputed_quartely)
    return final_spread_imputed_quartely


def addTSSheet(writer,dataframe,count):
    dataframe.to_excel(writer,'Treasury Spread {0}'.format(count),index=False)

def addTYSheet(writer,dataframe):
    dataframe.to_excel(writer,'Merging By Date'.format(count),index=False)

def get_negatives(x):
      if sum(x<0)==0 and sum(x>0)==0:
        return "nan" 
      else:
        return sum(x<0)



countries =['Argentina', 'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Belgium', 'Botswana', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'China', 'Colombia', 'Croatia', 
'Cyprus', 'Czech', 'Egypt', 'France', 'Germany', 'Greece', 'Hong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kenya',
 'Malaysia', 'Malta', 'Mauritius', 'Mexico', 'Morocco', 'Namibia', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar',
  'Romania', 'Russia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'Uganda', 'Ukraine',
   'United Kingdom', 'United States', 'Vietnam']

shortlisted_countries = ['United Kingdom', 'United States',"Japan","China","Canada","France","Germany","Singapore","Hong","South Korea", "Australia" ]
#uncomment  del Argentina

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
  if key in doneBCont:
    continue

  #Testing
  # if key not in shortlisted_countries:
  #   continue
  # if key != "China":
  #   continue
  # counter+=1
  # if counter >= len(countryNames)/8:
  #   break
  
  def mykey(value):
    if "(1)" in value:
      ls = value.split(" ")[-6]
      
    else:
      ls = value.split(" ")[-5]
    ia = ls.split("-")[1][0]
    return ia

  dd[key].sort(key=natural_keys)
  dd[key].sort(key=mykey)


  print("Working for {0} bonds".format(key))
  print("All Directories\n", dd[key])

  exit()

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
 
  ####################TEST FIELD###################
  
  parent_newBonds = []

  count = 1
  for x in range(0,len(bonds)-1):
    # print("Main Loop")
    newBonds = []
    for i in range(count,len(bonds)):
      
      # print("Inside Loop")
      # print(x , i)

      #Process
      xf = bonds[i].sub(bonds[x])
      xf = xf[~xf.index.duplicated()]
      xf = xf.fillna(value="na")
      newBonds.append(xf)
    
    parent_newBonds.append(newBonds)
    
    count += 1
  #print(parent_newBonds)


  resulx,sortex_df = extractingTreasuryYeilds(nbonds)
  writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
  writerRenamed = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))

  if key in shortlisted_countries:
    shortlist_sortex_df = shortlistedYeild(resulx)
    writerShorlisted = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
    writerShortlistedRenamed = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))

    mod_date_sortex_df, price_resulx,date_sortex_df = quarterlyInsightsYeild(resulx, resulx,0)
    imputed_yeild_df = ImputedYeild(mod_date_sortex_df)

    
    writerImputed = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
    writerQuarterly = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))




  # copy_sortex_df,copy_sorted_df = globalRename(sortex_df,sorted_df, aso)
  # sortex_df.to_excel(writer,'Merging By Date',index=False)
  # copy_sortex_df.to_excel(writer,'Merging By Date',index=False)


  # result,sorted_df = extractingTreasurySpreads(parent_newBonds[1],1)
  # print(result)



 


  aso = 0
  inc = 0
  for bonds in parent_newBonds:

    result,sorted_df = extractingTreasurySpreads(bonds,inc)
    copy_sortex_df,copy_sorted_df = globalRename(sortex_df,sorted_df, aso)

    
    addTYSheet(writer,sortex_df)
    addTSSheet(writer,sorted_df,aso)


    #Renamed
    addTYSheet(writerRenamed,copy_sortex_df)
    addTSSheet(writerRenamed,copy_sorted_df,aso)
    
    if key in shortlisted_countries: #not remo uncomment
      shortlist_sorted_df = shortlistedSpread(result)
      copy_shortlist_sortex_df,copy_shortlist_sorted_df = globalRename(shortlist_sortex_df,shortlist_sorted_df,aso)

      #Shortlisted
      addTYSheet(writerShorlisted,shortlist_sortex_df)
      addTSSheet(writerShorlisted,shortlist_sorted_df,aso)

      #Shorlisted Renamed
      addTYSheet(writerShortlistedRenamed,copy_shortlist_sortex_df)
      addTSSheet(writerShortlistedRenamed,copy_shortlist_sorted_df,aso)

      #Quarterly Insights
      mod_date_sorted_df = quarterlyInsightsSpread(result, price_resulx,date_sortex_df, aso)
      addTYSheet(writerQuarterly,mod_date_sortex_df)
      mod_date_sorted_dff = mod_date_sorted_df.replace("nan","na")
      addTSSheet(writerQuarterly,mod_date_sorted_dff,aso)

      #Imputed Quarterly

      final_spread_imputed_quartely = ImputedSpread(imputed_yeild_df, mod_date_sorted_df,aso)
      addTYSheet(writerImputed,imputed_yeild_df)
      addTSSheet(writerImputed,final_spread_imputed_quartely,aso)

     

      

    aso +=1
    inc += 2
  
  print("Writing Normal Files")
  os.chdir(main_path)
  os.chdir(output_path)
  writer.save()
  os.chdir(main_path)

  os.chdir(production_ouput_path)
  writerRenamed.save()
  os.chdir(main_path)

  if key in shortlisted_countries:
    print("Writing Shortlisted File", key)
  
    os.chdir(main_path)
    os.chdir(shortlist_output_path)
    writerShorlisted.save()
    os.chdir(main_path)

    os.chdir(shortlist_production_ouput_path)
    writerShortlistedRenamed.save()
    os.chdir(main_path)

    print("Writing Quarterly", key)

    os.chdir(quarterly_path)
    writerQuarterly.save()
    os.chdir(main_path)

    print("Writing Imputed Quarterly", key)

    os.chdir(imputed_quarterly_path)
    writerImputed.save()
    os.chdir(main_path)


  os.chdir(main_path)
  os.chdir(production_ouput_path)
  writeToCsv(dataDictd,"dataDictTreasurySpreads.csv")
  writeToCsv(dataDictx, "dataDictTreasuryYields.csv")
  os.chdir(main_path)
    



  
# exit()

  #-----------------------------

  #copy_sortex_df,copy_sorted_df = globalRename(sortex_df,sorted_df)


  # os.chdir(main_path)
  # os.chdir(output_path)
  # writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
  # sortex_df.to_excel(writer,'Merging By Date',index=False)
  # addTSSheet(writer,sortex_df,0)
  # writer.save()
  # os.chdir(main_path)

  
    


  # print(sortex_df)
  

  #GETTING CORRECT RESULTS
  #Now create a universal loop
  #Put things inside functions, slowly slowly , remain {Renamed,Shortlisted, Quarterly, Imputed}
  #-------------------Putting Things inside function slowly, slowly----

    # print(result)

  #------------------------

  # x = 0 , i = 1
  # x = 0 , i = 2
  # x = 1 , i = 2
  newBonds = []
  for i in range(0,len(bonds)):
    if i == 0:
      continue
    else:

      #Logic 2 >> 
      xf = bonds[i].sub(bonds[0])
      xf = xf[~xf.index.duplicated()]
      xf = xf.fillna(value="na")


      #find columns first to 3Year
      #for loop runs these times and referencing those columns
      #Checking conditions for subtract from lowest maturity
      # for loop to create sheets

      newBonds.append(xf)
  
  newBonds2 = []
  for i in range(0,len(bonds)):
    print(i)
    if i == 0 or i == 1:
      continue
    else:
      
      #Logic 2 >> 
      xf = bonds[i].sub(bonds[1])
      xf = xf[~xf.index.duplicated()]
      xf = xf.fillna(value="na")
      print("Loop end")

      newBonds2.append(xf)
  
  #newBonds
  print(newBonds2)
  exit()

  ###############################TEST FIELD END#################

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
  if key in shortlisted_countries:

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
    writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
    copy_shortlist_sortex_df.to_excel(writer,'Merging By Date',index=False)
    copy_shortlist_sorted_df.to_excel(writer,'Treasury Spread',index=False)
    writer.save()
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

    ## Quarter Done except Writing

    ##-------------------------- Imputed Quarterly -------------------

    ### YEILD
    imputed_yeild_df = mod_date_sortex_df.replace("na",numpy.nan).fillna(method='ffill').fillna("na")

    ### SPREADS ####
    #Subtracting YEilds for spread

    imput_y = imputed_yeild_df.replace('na',numpy.nan)
 

    x = imput_y.columns[1::2]
    y = imput_y.columns[2::2]




    avg = pd.DataFrame()

    #pd.set_option('display.max_rows', None)

    count =0
    for i in list(x):
      count+=1
      if count == 1:
        
        continue
      else:
        
        #subtracting every col with 2nd col (Avg Min)
        avg["avg{0}".format(count)] = imput_y[i] - imput_y.iloc[:,1]
    
    #print(avg)


    end = pd.DataFrame()
    count =0
    for i in list(y):
      count+=1
      if count == 1:
        
        continue
      else:
        
        #subtracting every column from third col (End min)
        end["end{0}".format(count)] = imput_y[i] - imput_y.iloc[:,2] #mistake here
    
    #print(end)

    avg_end = pd.merge(avg,end,left_index=True,right_index=True)


              #Renaming Avg End
    len_ae = len(avg_end.columns)/2
    len_ae = int(len_ae)
    z = mod_date_sorted_df.columns[1::4]
    a = mod_date_sorted_df.columns[2::4]
    
    
    naming = list(z)+list(a)
    # naming.pop(0)
    # naming.pop(int(len_ae))

    avg_end.columns = naming
    # print(avg_end)

          #FOR Min NEG
    
    spreads_train = mod_date_sorted_df.replace("na",numpy.nan)
    yx =  spreads_train.columns[3::4]
    xy =  spreads_train.columns[4::4]
    min_neg = spreads_train[list(xy)+list(yx)]
    print(min_neg)


          #MERGE AND ALIGN
    imp_spread = pd.merge(avg_end,min_neg,left_index=True,right_index=True)


    lst = []
    for i in range(len_ae):

      mod = imp_spread.columns[i::len_ae]
      lst += list(mod)

    print(lst)

    imp_spread = imp_spread[lst]
    #print(imp_spread)

          #Fill NA Min
    imp_spread = imp_spread.fillna(axis=1,limit=1,method="ffill")
    imp_spread=imp_spread.replace("nan",numpy.nan) #Uncomment Check

    #print(imp_spread)

    


          #NEg Jugaar

   
    #1.234 and 0.0 in last list
    #imp_spread = imp_spread.fillna("na") #check
    colNames = imp_spread.columns
    listOfDFRows = imp_spread.to_numpy().tolist()
    #print(listOfDFRows)
    for currCol in range(1,len(listOfDFRows)):
      #print(listOfDFRows[currCol])
      for col in range(1,len(listOfDFRows[currCol])):
          if math.isnan(listOfDFRows[currCol][col]):
            #print(listOfDFRows[currCol])
            if listOfDFRows[currCol][col-1] < 0:
              listOfDFRows[currCol][col] = 1
            elif listOfDFRows[currCol][col-1] > 0:
              listOfDFRows[currCol][col] = 0
          # if listOfDFRows[currCol][col] == "alpha" and listOfDFRows[currCol][col-1] != "alpha" and listOfDFRows[currCol][col-1] != "na":

          # if listOfDFRows[currCol][col] == "alpha" and listOfDFRows[currCol][col-1] != "alpha" and listOfDFRows[currCol][col-1] != "na":
          #   if listOfDFRows[currCol][col-1] < 0:
          #     listOfDFRows[currCol][col] = 1
          #   elif listOfDFRows[currCol][col-1] > 0:
          #     listOfDFRows[currCol][col] = 0
      #output one row list

    #ouput list of rows
    print(len(listOfDFRows))

    imputed_spread = pd.DataFrame(listOfDFRows)
    imputed_spread.columns = colNames
    #print(xx)

    

    
    


          #Add Date Col
    date = mod_date_sorted_df.columns[0]
    date = mod_date_sorted_df[date]
    imputed_spread.insert(0, "Date", date)
    
    # imputed_spread = pd.merge(date,imp_spread,left_index=True,right_index=True)
    # print(imputed_spread)
    print(imputed_spread)

        #Writing


    final_spread_imputed_quartely = mod_date_sorted_df.copy(deep=True)
    final_spread_imputed_quartely = final_spread_imputed_quartely.replace("na",numpy.nan).replace("nan",numpy.nan)
    #final_spread_imputed_quartely[final_spread_imputed_quartely.isnull()] = imputed_spread.values
    final_spread_imputed_quartely=final_spread_imputed_quartely.fillna(imputed_spread)



    final_spread_imputed_quartely = final_spread_imputed_quartely.fillna("na")

    print(final_spread_imputed_quartely, "df1")
    print(imputed_spread, "df2")
    print(final_spread_imputed_quartely)

    #exit()

    #imputed_spread = imputed_spread.fillna("na")
    os.chdir(main_path)
    os.chdir(imputed_quarterly_path)
    writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
    imputed_yeild_df.to_excel(writer,'Merging By Date',index=False)
    # imputed_spread.to_excel(writer,'Treasury Spread',index=False)
    final_spread_imputed_quartely.to_excel(writer,'Treasury Spread',index=False)

    writer.save()
    os.chdir(main_path)

    print("Done Quarterly Imputations For",key)






    # print(liy)
    










    
    #Renaming col names , add date columns
    #Not chnaging below code , will se it later, maybe delete in end
    #Negatives jugaar
    
    
    


    
    #Uncomment remove continue

    #Run it only for imputed quarteryl (and send), then all shortlisted_countries list, then upto 3-4 coountries for ALL to check the flow

    mod_date_sorted_df = mod_date_sorted_df.replace("nan","na")

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
  # -----------------------------------------------Imputed/Quarterly Insights Ends-------------
  
  

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

  #Uncomment , Check this
  writeToCsv(dataDictd,"dataDictTreasurySpreads.csv")
  writeToCsv(dataDictx, "dataDictTreasuryYields.csv")






  os.chdir(main_path)






# print(dataDictd)
# print(dataDictx)






exit()


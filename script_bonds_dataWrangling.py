import csv
import os
import glob
import time

f = open('Part1.csv', 'w',newline='')
with f:
    writer = csv.writer(f)
    writer.writerow(["Countries","1st starting date","1st ending date","2nd starting date","2nd ending date"])


#Variables
countryNamesSliced=[]
countries = []


path = os.getcwd()
extension = 'csv'
os.chdir(path)
countryNames = glob.glob('*.{}'.format(extension))


print(countryNames)
exit()


rowToWrite = []
rowOfrows = []
count = 0
for countryName in countryNames:
    count += 1
    
    
    if count == 3:
        rowOfrows.append(rowToWrite)
        rowToWrite = []
        count = 1
        
    
    # print(count)
    if count < 3:
        # print(countryName)
        rowList = []
        with open(countryName, newline='', encoding='latin-1') as f:
            
            reader = csv.reader(f)

            for row in reader:
                rowList.append(row)
        
        
            
        endDate = rowList[1][0]
        startDate = rowList[-1][0]

        if count != 2:
            rowToWrite.append(countryName)
        rowToWrite.append(startDate)
        rowToWrite.append(endDate)

        
    if countryNames.index(countryName)==len(countryNames)-1:
        
        rowOfrows.append(rowToWrite)
        
        
    

print("Data",rowOfrows)

f = open('Part1.csv', 'a+',newline='')
with f:
    writer = csv.writer(f)
    writer.writerows(rowOfrows)
    # for row in rowOfrows:
    #     writer.writerow(row)
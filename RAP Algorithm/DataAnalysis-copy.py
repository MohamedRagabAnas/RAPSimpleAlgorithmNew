import csv
import pandas as pd
import numpy as np
import requests
import json
import sys
import re

def readReviwerscsv(CSVFile):
	df=pd.read_csv(CSVFile)
	df.Affiliation=df.Affiliation.apply(lambda x: x[1:-1].split(','))
	df.Affiliation = [tuple(lst) for lst in df.Affiliation]
	#df=df.assign(Affiliation=df.Affiliation.str.strip('[]').str.split(','))
	return df

def readAuthorscsv(CSVFile):
	df=pd.read_csv(CSVFile)
	df.Affiliations=df.Affiliations.apply(lambda x: x[1:-1].split(','))
	df.Affiliations = [tuple(lst) for lst in df.Affiliations]
	#df=df.assign(Affiliations=df.Affiliations.str.strip('[]').str.split(','))
	df.Co_Authors=df.Co_Authors.apply(lambda x: x[1:-1].split(','))
	df.Co_Authors = [tuple(lst) for lst in df.Co_Authors]
	return df

def filterCitations(df):
	df=df.drop(df[(df.CitedBy <20) | (df.CitedBy>1000) ].index)
	#df=df.ix[(df['citedby'] >= 100) & (df['citedby']<=1000)]
	return df

def excludeCOIs(Revdf,Authdf):
	# get rid of COIs (Reviewer : not one of authors, no co-work or afilliations, not in a same country)
	Revdf=Revdf[~Revdf.Name.isin(Authdf.Names.values)] # Crisp Name Matching... we need to check the fuzzy wuzzy or alternatives here...
	
	'''AFFFAuth=[]
	AFFFRev=[]

	for i in range (len(Authdf.Affiliations)):
		AffAuth=Authdf.Affiliations[i].strip('[]').split(',')
		AFFFAuth.append(AffAuth)
	print AFFFAuth	
	
	for i in range (len(Revdf.Affiliation)):
		AffRev = Revdf.Affiliation[i].strip('[]').split(',')
		AFFFRev.append(AffRev)
	print AFFFRev

	for  afflist in AFFFRev:
		result =  any(elem in afflist  for elem in AFFFAuth)
		print result,'\n'
	'''	
	Revdf=Revdf[~Revdf.Name.isin(Authdf.Co_Authors.values)]

	Revdf=Revdf[~Revdf.Affiliation.isin(Authdf.Affiliations.values)]
	#print Authdf.Affiliations.values[0]

	#Revdf=Revdf[~Revdf.Affiliation.isin(Authdf.Affiliations[0])]
	
	return Revdf

def main():
    
    Reviewersdf= readReviwerscsv(sys.argv[1])
    print(len(Reviewersdf.index))

    Authorsdf= readAuthorscsv(sys.argv[2])
    print(len(Authorsdf.index))
    
    Reviewersdf=filterCitations(Reviewersdf)
    print(len(Reviewersdf.index))

    #Reviewersdf.Affiliation=Reviewersdf.Affiliation.apply(lambda x: x[1:-1].split(','))
    #print (Reviewersdf.Affiliation[0][0])
    #print (Authorsdf.Affiliations[0][1])
    
    '''result=any(elem in  Authorsdf.Affiliations[0] for elem in Reviewersdf.Affiliation[4])
    print result'''

    #print Reviewersdf.Affiliation[4]
    #print Authorsdf.Affiliations[0]	

    exdf=excludeCOIs(Reviewersdf,Authorsdf)
    print(len(exdf.index))
    print(exdf.Name)

if __name__ == '__main__':
    main()
import os, sys, re, sqlparse, csv

#####################################################################################################################
def is_int(s):
	# helper function to check if a string, s, is an integer, positive or negative
    try: 
        int(s)
        return True
    except ValueError:
        return False

#####################################################################################################################

class table:
	def __init__(self, name, clmns):
		# error handling to check if the csv file can be opened
		try:
			# error handling to check if the particular table csv file is in the directory
			if str(name+".csv") not in os.listdir("."):
				print("Error\nFile missing\n"+name+".csv not found in the current directory")
				exit()
			
			# permission issues might persist, hence the try-except block

			self.name, self.clmns, self.data = name, clmns, []
			with open(name+".csv", "r") as lmao:
				for row in csv.reader(lmao):
					self.data.append([int(i) for i in row])
			
			# for i in range(len(clmns)):
			# 	self.clmns[i] = self.name+'.'+self.clmns[i]
		
		except:
			print("Error while opening "+name+".csv file")
			exit()
	def prntTbl(self):
		# print the particular table in the db
		print(self.name)
		print(self.clmns)
		print(self.data)

class database:
	def __init__(self):

		try:
			# error handling: to check if metadata.txt is there in the directory
			if "metadata.txt" not in os.listdir("."):
				print("Error\nmetadata.txt not found in the current directory")
				exit()

			self.tblNms, self.tbls, tmpLst = [], [], []

			with open('metadata.txt', 'r') as r:
				flg = 0
				for i in r:
					i = i.strip()
					if i == '<begin_table>':
						flg = 1
					elif flg:
						self.tblNms.append(i)
						flg = 0
					elif i == '<end_table>':
						self.tbls.append(table(self.tblNms[-1], tmpLst))
						tmpLst = []
					else:
						tmpLst.append(i)
		except:
			print("Error while opening metadata.txt file")
			exit()
	def prntDb(self):
		# print the whole database
		print(self.tblNms)
		for t in self.tbls:
			t.prntTbl()

#####################################################################################################################

def getTbls(tblsLst):
	tbls= []
	tblNms = [x.strip() for x in tblsLst.strip().split(',\n')]

	for tbl in tblNms:
		if tbl not in DB.tblNms:
			print("Requested data not found\nTable"+tbl+" not in database")
			exit()
		tbls.append(DB.tbls[DB.tblNms.index(tbl)])
	return tbls

def getData(tbls):
	
	# if there's only one table, return its data directly
	if (len(tbls) == 1):
		return tbls[0].data
	
	# if there're more than one, get all combinations of the tables possible iteratively
	else:
		prevData = tbls[0].data
		currData = []
		for t in range(1,len(tbls)):
			tbl_t = tbls[t].data
			currData = []
			for i in range(len(prevData)):
				for j in range(len(tbl_t)):
					currData.append(prevData[i]+tbl_t[j])
			prevData = currData
		return currData

#####################################################################################################################

def getStrngLst(qry):
	# to check for syntax errors
	# returns a list of strings 

	# check if there is a semicolon at the end of the query. if not, it is an invalid query
	if(qry[-1] != ';'):
		print("Invalid Query\nSystax error\nExpected \';\' at the end of the query\nShould be in the form:")
		print("SELECT (DISTINCT) <col1, col2, ...> FROM <table_name> (WHERE <conditions>);")
		return

	# make all uppercase and reformat into different lines. semicolon is no longer useful for further steps, so remove that
	qry = sqlparse.format(qry, reindent=True, keyword_case = 'upper')[:-1]
	# get encoding of the query/ies
	qry = sqlparse.parse(qry)

	# we only have to deal with one query at a time. multiple queries are not given in a single input [as given in the problem statement]
	qry = qry[0]
	# get tokens of the query
	qry = qry.tokens
	# get identifiers from the query
	qry = sqlparse.sql.IdentifierList(qry).get_identifiers()
	# get identifiers from the query, and make a list of strings from the query
	prsdQry = []
	for sub in qry:
		prsdQry.append(str(sub))
	
	# print(prsdQry)
	
	# check for syntax errors. where statement syntax check done later
	if (len(prsdQry)<4):
		print("Invalid Query\nShould be in the form:\nSELECT (DISTINCT) <col1, col2, ...> FROM <table_name> (WHERE <conditions>);")
		exit()
	elif (prsdQry[0] != "SELECT"):
		print("Invalid Query\nMissing \'Select\' term\nShould be in the form:\nSELECT (DISTINCT) <col1, col2, ...> FROM <table_name> (WHERE <conditions>);")
		exit()
	elif (prsdQry[2] != "FROM" or (prsdQry[1]=="DISTINCT" and prsdQry[3]!="FROM")):
		print("Invalid Query\nMissing \'FROM\' term\nShould be in the form:\nSELECT (DISTINCT) <col1, col2, ...> FROM <table_name> (WHERE <conditions>);")
		exit()

	return prsdQry

#####################################################################################################################

def gtCndtnDt(dtClmns, tbls, data, fllCndtn, prtsOfCndtn):

	# handling if the condition has only one part
	if len(prtsOfCndtn) == 1:
		# print(prtsOfCndtn)
		if prtsOfCndtn[0][:2] == "OR":
			prtsOfCndtn[0] = prtsOfCndtn[0][2:].strip()
		elif prtsOfCndtn[0][:3] == "AND":
			prtsOfCndtn[0] = prtsOfCndtn[0][3:].strip()
		if (not is_int(prtsOfCndtn[0])):
			print("Invalid query\nIn the condition:\n"+fllCndtn+"\nThere is no comparison of a value with another")
			exit()
		# if the condition is just a number, output all the data as if this particular condition didnt exist
		if is_int(prtsOfCndtn[0]):
			return data
		else:
			return []
	
	# makes a list from ['table1.A', 'table2.B'] --to--> [['A', 'table1'], ['B', 'table2']]
	prtsOfCndtn = [i[::-1] for i in [i.split(".") for i in [column.strip() for column in prtsOfCndtn]]]

	clmnIndx, newData = [], []
	for prt in prtsOfCndtn:
		if len(prt) == 2:
			# if the part of the condition is of the form table1.A, then this is used to handle that
			fndFlg = False
			for table in tbls:
				if prt[1] == table.name:
					# checking if the requested table is in the list of tables in from clause
					fndFlg = True
			if not fndFlg:
				# if it isnt found, get the fok outta there
				print("Invalid Query\nUnknown table \'"+prt[1]+"\'")
				exit()
			if not prt[0] in DB.tbls[DB.tblNms.index(prt[1])].clmns:
				# if the requested attribute is not found in the colmns of the requested table, get the fok outta there
				print("Invalid Query\nUnknown attribute \'"+prt[0]+"\' being called from the table \'"+prt[1]+"\'")
				exit()
		
		if not is_int(prt[0]) and not prt[0] in dtClmns:
			# if its just a single table attribute, and it isnt found in the columns of the table in from clause
			print("Invalid Query\nUnknown attribute \'"+prt[0]+"\' being called from the table \'"+prt[1]+"\'")
			exit()
		
		if is_int(prt[0]):
			# if the condition part is just an integer
			clmnIndx = clmnIndx + ['num']
		else:
			# if it aint one, find the required column indices of the requested attribute
			indcs = []
			for itr in range(len(dtClmns)):
				if prt[0] == dtClmns[itr]:
					indcs.append(itr)
			
			if len(indcs) == 1:
				# if requested for a single column, and it be found, just add it
				clmnIndx = clmnIndx + [indcs[0]]
			else:
				if len(prt) == 1:
					# if of form just <attr_name>, but has ended up here, then that means that there are multiple attributes with this name prt[0]
					# and cant confirm which is the one required. much confuse
					print("Invalid Query\nUnknown attribute \'"+prt[0]+"\'")
					exit()
				else:
					# now find which is the exact index of the column of that table we request data from
					pstn = 0
					for table in tbls:
						if prt[0] in table.clmns:
							if table.name != prt[1]:
								pstn+=1
							else:
								break
					clmnIndx += [indcs[pstn]]

	if (not clmnIndx[0] == 'num') and (not clmnIndx[1] == 'num') and "=" in fllCndtn:
		jnFlg = True
		jnIndcs = clmnIndx

	for row in data:

		val1 = int(prtsOfCndtn[0][0]) if (clmnIndx[0] == 'num') else row[clmnIndx[0]]
		val2 = int(prtsOfCndtn[1][0]) if (clmnIndx[1] == 'num') else row[clmnIndx[1]]
		appndFLg = False

		if ">=" in fllCndtn:
			if val1 >= val2:
				appndFLg = True

		elif "<=" in fllCndtn:
			if val1 <= val2:
				appndFLg = True

		elif "<" in fllCndtn:
			if val1 < val2:
				appndFLg = True

		elif ">" in fllCndtn:
			if val1 > val2:
				appndFLg = True

		elif "=" in fllCndtn:
			if val1 == val2:
				appndFLg = True

		else:
			print("Err: Invalid condition in WHERE")
			exit()

		if appndFLg:
			newData.append(row)

	return newData

def cndtnHndlr(cndtns, tbls, dt, dtClmns):

	cndtns = [i.strip() for i in cndtns.split('\n')]
	
	# only 2 conditions are acceptable at max, according to problem statement
	if len(cndtns) > 2:
		print("Invalid query\nOnly 2 conditions can be given, linked with an AND or an OR operator only")
		exit()

	orFlg, andFlg, snglCndtnFlg = False, False, True
	dt1, dt2 = [],[]


	# print(cndtns)
	dt1 = gtCndtnDt(dtClmns, tbls, dt, cndtns[0][6:], re.split(r'[=><]+',cndtns[0][6:]))
	# handling second condition and the logical operator
	if len(cndtns) > 1:
		snglCndtnFlg = False
		if ("OR" in cndtns[1] or "AND" in cndtns[1]):
		
			if "OR" == cndtns[1][:2]:
				orFlg, cndtns[1] = True, cndtns[1][3:]
			elif "AND" == cndtns[1][:3]:
				andFlg, cndtns[1] = True, cndtns[1][4:]

			dt2 = gtCndtnDt(dtClmns, tbls, dt, cndtns[1], re.split(r'[=><]+',cndtns[1]))
		
		else:
			print("Invalid query\nOnly AND or OR logical operator can be used")
			exit()

	# to remove the 'where ' string from the query
	cndtns[0] = cndtns[0][6:]

	if snglCndtnFlg:
		return dt1
	else:
		newData = []
		for row in dt:
			if andFlg and (row in dt1 and row in dt2):
				newData.append(row)
			elif orFlg and (row in dt1 or row in dt2):
				newData.append(row)
		return newData

#####################################################################################################################

def slctHndlr(dtClmns, data, slctOpts, dstnctFlg):

	slctOpts = [x.strip() for x in slctOpts.split(",")]
	# print(slctOpts)

	if len(slctOpts) == 1:
		slctOpts = re.split(r'[\ \(\)]+',slctOpts[0])
		slctOpts = list(filter(None, slctOpts))
		# print(slctOpts)
		if(slctOpts[0].upper() in ["SUM", "MAX", "MIN", "AVG"]):
			slctOpts[0] = slctOpts[0].upper()
			if slctOpts[1] not in dtClmns:
				print("Invalid Command\nThe column "+slctOpts[1]+" is not present in the table")
				exit()
				
			else:
				if "SUM" == slctOpts[0]:
					i = dtClmns.index(slctOpts[1])
					tmp = [row[i] for row in data]
					print("SUM("+slctOpts[1]+") =\n"+str(sum(tmp)))
					exit()
				elif "MAX" == slctOpts[0]:
					i = dtClmns.index(slctOpts[1])
					tmp = [row[i] for row in data]
					print("MAX("+slctOpts[1]+") =\n"+str(max(tmp)))
					exit()
				elif "MIN" == slctOpts[0]:
					i = dtClmns.index(slctOpts[1])
					tmp = [row[i] for row in data]
					print("MIN("+slctOpts[1]+") =\n"+str(min(tmp)))
					exit()
				elif "AVG" == slctOpts[0]:
					i = dtClmns.index(slctOpts[1])
					tmp = [row[i] for row in data]
					avg=sum(tmp)/len(tmp)
					print("AVG("+slctOpts[1]+") =\n"+str(avg))
					exit()

	sctdIndcs, rqdDt = [], []
	
	if slctOpts[0] == '*':
		# select all in the data columns for the selected tables
		slctOpts = dtClmns
	
	for q in slctOpts:
		if q not in dtClmns:
			# if requested column is not in the query
			print("Invalid query\nThe field \'"+q+"\' not found in the mentioned tables")
			exit()

		indcs = []
		for itr in range(len(dtClmns)):
			if q == dtClmns[itr]:
				indcs.append(itr)
		sctdIndcs = sctdIndcs + indcs
	
	# printing column names
	for i in range(len(slctOpts)):
		if (not jnFlg or (jnFlg and not i == jnIndcs[1])):
			print(slctOpts[i],end="\t|")
	print()

	# printing the requested data
	for i in range(len(slctOpts)):
		print("____",end="\t|")
	print()
	for row in data:
		row1 = []
		for i in range(len(row)):
			if i in sctdIndcs and ((not jnFlg) or (jnFlg and not i == jnIndcs[1])):
				row1 = row1 + [row[i]]
		
		if not dstnctFlg:
			rqdDt.append(row1)
		elif row1 not in rqdDt:
			rqdDt.append(row1)

	# printing the data onto the terminal
	for row in rqdDt:
		for i in range(len(row1)):
			print(str(row[i]),end="\t|")
		print()

	return

#####################################################################################################################

def qryEngn(qry):

	qry = getStrngLst(qry)
	whrFlg, dstnctFlg = False, False

	if(qry[2]=="FROM"):
		tbls = getTbls(qry[3])
		if len(qry) >= 5:
			whrFlg = True

	elif(qry[2]=="DISTINCT"):
		dstnctFlg, tbls = True, getTbls(qry[4])
		if len(qry) >= 6:
			whrFlg = True
	
	data = getData(tbls)

	# get the attribute names of all tables
	dtClmns = []
	for i in tbls:
		dtClmns += i.clmns
	# for i in tbls:
	# 	tmp = []
	# 	for j in i.clmns:
	# 		tmp.append(i.name+'.'+j)
	# 	dtClmns += tmp

	if whrFlg:
		data = cndtnHndlr(qry[-1], tbls, data, dtClmns)
	if dstnctFlg:
		slctHndlr(dtClmns, data, qry[2], dstnctFlg)
	else:
		slctHndlr(dtClmns, data, qry[1], dstnctFlg)


#####################################################################################################################

if(len(sys.argv) != 2):
	print("Invalid format of the command\nIt should be in the form:\npython 20171404.py \"select * from table_name where condition;\"")
	exit()
DB = database()
jnFlg, jnIndcs = False, []
qryEngn(sys.argv[1])
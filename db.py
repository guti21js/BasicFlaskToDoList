import mysql.connector as mariadb


def initialize():
	conn =mariadb.connect(host='todolistdb.cnjllkigqfjv.us-east-1.rds.amazonaws.com',
							database ='todolistdb',
							user='appuser',
							password='#1Shingeki'
						)
							
	cur=conn.cursor(buffered=True)
				
	return cur,conn
	
	
	
def createuser( user, cursor, connection):
	

	sql_checkuser="SELECT User FROM user_table WHERE User = %s"
	data=(user,)
	result= cursor.execute(sql_checkuser,data)
	
	
	print(result)
	if result is None:
		sql_createuser="INSERT INTO user_table (User,ID) VALUES (%s,%s)"
		data=(user,"")
		try: 
			result= cursor.execute(sql_createuser,data)
			connection.commit()
			return("Insert Good")
		except Exception as e:
			return(str(e))
	else:
		return(False)

		
def finduser( user, cursor, connection): ##checks if user was found/exists, returns error if it doesn't
	


	sql_finduser="SELECT user FROM user_table WHERE user = %s"
	data=(user)
	
	try: 
		result= cursor.execute(sql_createuser,data)
		connection.commit()
		return("Find Good")
	except Exception as e:
		return(str(e))
		
		
		
		
def getlist( user, cursor, connection):
	


	sql_finduser="SELECT * FROM items WHERE user = %s"
	data=(user,)
	
	try: 
		cursor.execute(sql_createuser,data)
		##connection.commit()
		myresult=cursor.fetchall()
		print("get list good")
		
		print(len(myresult))
		
		for x in myresult:
			print(x)
		
		return(myresult)
	except Exception as e:
		return(str(e))
'''def loginuser( user, cursor, connection):
	


	sql_createuser="SELECT* FROM items WHERE user = %s"
	data=(user)
	
	try: 
		result= cursor.execute(sql_createuser,data)
		connection.commit()
		return("Insert Good")
	except Exception as e:
		return(str(e)) '''
		
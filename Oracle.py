import cx_Oracle as db
db.init_oracle_client(lib_dir=r"C:\\oracle\\instantclient_12_1")
from config import login



class dbQuery():
    def __init__(self, querystring='', user= login['user'], password = login["password"], dsn = login['dsn'], ):
        self.user = user
        self.password = password
        self.dsn = dsn
        self.querystring = querystring

    @property
    def connection(self):
       return db.connect( user = self.user, 
                    password = self.password, 
                    dsn = self.dsn)
        
    @property
    def orders(self):
        cursor = self.connection.cursor()
        cursor.execute(self.querystring)
        self.headers = cursor.description
        cursor.rowfactory = lambda *args: dict(zip([d[0] for d in cursor.description],args))
        return(cursor.fetchall())



    


if __name__ == "__main__":
    
    z = conn.search("select * from AMH50.Z68 " + "where ROWNUM < 10") 
    

   
    
      

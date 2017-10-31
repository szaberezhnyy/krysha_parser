import cx_Oracle

con = 0
cur = 0


def open_connection():
	global con, cur
	con = cx_Oracle.connect('qwer/123@127.0.0.1/xe')
	cur = con.cursor()
	

def close_connection():
	global con
	con.close()


def create_table_of_flats():
	cur.execute('''CREATE TABLE Flat_info (id int, link varchar2(50),	
		city varchar2(50), district varchar2(50), mcr_district varchar2(50),
		address varchar2(50), floor_num int, max_floor_num int, room_number int,
		square number(5), price number(5), description varchar2(500), update_date varchar2(50))''')
	cur.execute("ALTER TABLE Flat_info ADD (CONSTRAIT flat_pk PRIMARY KEY (id))")
	cur.execute("CREATE SEQUENCE flat_seq START WITH 1")
	cur.execute('''CREATE OR REPLACE TRIGGER flat_on_insert
  BEFORE INSERT ON Flat_info
  FOR EACH ROW
BEGIN
  SELECT flat_seq.nextval
  INTO :new.id
  FROM dual;
END ''')
	cur.execute("COMMIT")


def drop_table(table_name):
	cur.execute("DROP TABLE :1", table_name)
	cur.execute("COMMIT")


def truncate_table():
	cur.execute("TRUNCATE TABLE :1", table_name)
	cur.execute("COMMIT")


def create_table_of_urls():
	cur.execute('''CREATE TABLE queries (url_id int, url varchar2(50), time_of_querie date)''')
	cur.execute("ALTER TABLE queries ADD (CONSTRAIT url_pk PRIMARY KEY (url_id))")
	cur.execute("CREATE SEQUENCE url_seq START WITH 1")
	cur.execute('''CREATE OR REPLACE TRIGGER flat_on_insert
  BEFORE INSERT ON queries
  FOR EACH ROW
BEGIN
  SELECT url_seq.nextval
  INTO :new.url_id
  FROM dual;
END ''')
	cur.execute("COMMIT")
	

def insert_into_flats(link,	city, district, mcr_district,address, floor_num, max_floor_num,
 room_number, square, price, description, update_date):
	cur.execute('''INSERT INTO Flat_info (link,	city, district, mcr_district,
		address, floor_num, max_floor_num, room_number,
		square, price, description, update_date) 
		VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12) ''', (link,	city, district,
		 mcr_district,address, floor_num, max_floor_num, room_number, square, price, 
		 description, update_date))
	cur.execute('COMMIT')


def insert_into_urls(url):
	cur.execute('INSERT INTO queries (url, time_of_querie) VALUES (:1, SYSDATE)', url)
	cur.execute('COMMIT')
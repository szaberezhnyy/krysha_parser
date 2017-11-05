import cx_Oracle

con = 0
cur = 0


def open_connection():
    global con, cur
    con = cx_Oracle.connect('serg/123@127.0.0.1/xe')
    cur = con.cursor()


def close_connection():
    global con
    con.close()


def create_table_of_flats():
    cur.execute('''CREATE TABLE Flat_info (id int, link varchar2(500),	
        city varchar2(500), district varchar2(500), mcr_district varchar2(500),
        address varchar2(500), floor_num int, max_floor_num int, room_number int,
        square number(5), price number(5), description varchar2(1000), update_date varchar2(500), url varchar(300))''')
    cur.execute("ALTER TABLE Flat_info ADD (CONSTRAINT flat_pk PRIMARY KEY (id))")
    cur.execute("ALTER TABLE Flat_info ADD (CONSTRAINT flat_fk FOREIGN KEY (url) REFERENCES urls (url))")
    try:
        cur.execute("DROP SEQUENCE flat_seq")
    except:
        pass    
    cur.execute("CREATE SEQUENCE flat_seq START WITH 1 INCREMENT BY 1 ORDER")
    cur.execute('''CREATE OR REPLACE TRIGGER flat_on_insert
  BEFORE INSERT ON Flat_info
  FOR EACH ROW
BEGIN
  SELECT flat_seq.nextval
  INTO :new.id
  FROM dual;
END; ''')
    cur.execute("COMMIT")



def drop_table_flat_info():
    cur.execute("DROP TABLE flat_info")
    cur.execute("COMMIT")

    
    
def drop_table_urls():
    cur.execute("DROP TABLE urls")
    cur.execute("COMMIT")



def truncate_table(table_name):
    cur.execute("TRUNCATE TABLE :tab", tab=table_name)
    cur.execute("COMMIT")



def create_table_of_urls():
    cur.execute('''CREATE TABLE URLS (url varchar2(300), date_of_querie date)''')
    cur.execute("ALTER TABLE URLS ADD (CONSTRAINT url_pk PRIMARY KEY (url))")    
    cur.execute("COMMIT")


def insert_into_flats(link, city, district, mcr_district, address, floor_num, max_floor_num,
 room_number, square, price, description, update_date, url):
    cur.execute('''INSERT INTO Flat_info (link, city, district, mcr_district,
        address, floor_num, max_floor_num, room_number,
        square, price, description, update_date, url) 
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13) ''', (link, city, district,
         mcr_district,address, floor_num, max_floor_num, room_number, square, price, 
         description, update_date, url))
    cur.execute('COMMIT')


def insert_into_urls(url):
    tup = (url,)
    cur.execute("INSERT INTO URLS  VALUES (:1, sysdate)",tup)
    cur.execute('COMMIT')

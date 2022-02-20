import sqlite3
from datetime import *

class DB_Manager():
    def __init__(self, db_name):
        self.db_name = db_name
        # self.conn = sqlite3.connect("db/" + str(self.db_name) + '.db')  # connection 생성
        # self.cur = self.conn.cursor()  # connection을 통해서 cursor를 넣어줘야 함

    # def __del__(self):  # 소멸자
    #     # self.conn.commit()  # 반영하자
    #     self.conn.close()  # 커넥션 닫기

    def create_table(self, table_name, dict_fields):

        ins_sql = "create table if not exists " + str(table_name) + "("     # 'ins_sql' example: 'create table ?(title text, pubd text, pus text, page integer, re integer)'
        for key, val in dict_fields.items():
            ins_sql = ins_sql + str(key) + ' ' + str(val) + ', '
        ins_sql = ins_sql[:-2]
        ins_sql = ins_sql + ')'

        self.conn = sqlite3.connect("db/" + str(self.db_name) + '.db')  # connection 생성
        self.cur = self.conn.cursor()  # connection을 통해서 cursor를 넣어줘야 함
        self.cur.execute(ins_sql)
        self.conn.commit()
        self.conn.close()  # 커넥션 닫기

    def insert_data(self, table_name, data):
        self.conn = sqlite3.connect("db/" + str(self.db_name) + '.db')  # connection 생성
        self.cur = self.conn.cursor()  # connection을 통해서 cursor를 넣어줘야 함
        for row in data.itertuples():
            ins_sql = "insert into " + str(table_name) + "("
            for key in data.keys():
                ins_sql = ins_sql + str(key) + ", "
            ins_sql = ins_sql[:-2] + ") values (?, ?, ?, ?, ?, ?)"
            self.cur.execute(ins_sql, (str(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6])))
        self.conn.commit()
        self.conn.close()  # 커넥션 닫기


    # def insert_data(self):
    #
    #     self.cur.execute("insert into test values('개발자의 코드', '2016-05-26', 'a', 200, 0)")  # 정적 쿼리
    #
    #     ins_sql = 'insert into test values(?,?,?,?,?)'  # 동적 쿼리. ?에 들어갈 내용을 모름
    #     self.cur.execute(ins_sql, ('클린코드', '2016-04-04', 'b', 300, 1))  # 동적 쿼리. ?에 들어갈 내용 지정
    #
    #     books = [('한국사', '2016-02-02', 'c', 330, 1), ('물리개론', '2015-01-04', 'a', 130, 0),
    #              ('건축학', '2013-10-14', 'e', 150, 0)]
    #     self.cur.executemany(ins_sql, books)  # 리스트로 여러개의 데이터를 한 번에 넣고 싶을 때 사용

    def parse_dt_border(self, table_name):
        ins_sql_last = 'select max(datetime) from ' + table_name
        ins_sql_first = 'select min(datetime) from ' + table_name



        try:
            self.conn = sqlite3.connect("db/" + str(self.db_name) + '.db')  # connection 생성
            self.cur = self.conn.cursor()  # connection을 통해서 cursor를 넣어줘야 함
            self.cur.execute(ins_sql_first)
            for res in self.cur:
                datetime_first = res

            self.cur.execute(ins_sql_last)
            for res in self.cur:
                datetime_last = res

            self.conn.commit()
            self.conn.close()  # 커넥션 닫기

            if datetime_first[0] == None or datetime_last[0] == None :       # 테이블은 존재하나, 데이터가 없을 때 None이 출력됨
                return False

            datime_border = {'first': datetime_first[0], 'last' : datetime_last[0]}
            return datime_border
        except:     # 테이블 자체가 없는 경우(대부분)
            return False


    def select_all(self):
        self.cur.execute('select * from test where title = "한국사"')  # 커서에 쿼리 실행
        print('[1] 전체 데이터 출력하기')

        rs = self.cur.fetchall()  # 커서에 조회된 모든 것을 페치함
        for book in rs:
            print(book)

    def select_n(self, n):
        self.cur.execute('select * from test where title = "한국사"')  # 커서에 쿼리 실행
        print('[2] 일부 데이터 출력하기')

        rs = self.cur.fetchmany(n)  # 커서에 조회된 것 중 n개의  데이터만 가져와라
        for book in rs:
            print(book)

    def update_data(self):
        up_sql = 'update test set title=? where title=?'
        self.cur.execute(up_sql, ('중국사', '한국사'))  # 중국사를 한국사로 변경
        self.conn.commit()

    def delete_data(self):
        del_sql = 'delete from test where title=?'
        self.cur.execute(del_sql, ('중국사',))  # 튜플 형태
        self.conn.commit()

    def asis_db_validity(self, db_datatime_last, timeframe):

        now = datetime.now()
        cnt = int(timeframe[:-1])
        factor = timeframe[-1]

        if factor == 'm':
            basis = now - timedelta(minutes=cnt)
        elif factor == 'h':
            basis = now - timedelta(hours=cnt)
        elif factor == 'd':
            basis = now - timedelta(days=cnt)
        elif factor == 'w':
            basis = now - timedelta(weeks=cnt)
        elif factor == 'M':
            basis = now - timedelta(weeks=4)
        else:
            basis = 0
            print('wtf!!!')

        if db_datatime_last > basis:
            return False
        else:
            return True

        return validity
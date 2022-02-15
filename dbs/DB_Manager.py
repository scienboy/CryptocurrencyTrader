import sqlite3

class DB_Manager():
    def __init__(self, db_name):
        # self.conn = sqlite3.connect("db/testdb.db")   # connection 생성
        self.conn = sqlite3.connect("db/" + str(db_name))  # connection 생성
        self.cur = self.conn.cursor()  # connection을 통해서 cursor를 넣어줘야 함

    def __del__(self):  # 소멸자
        self.conn.commit()  # 반영하자
        self.conn.close()  # 커넥션 닫기

    def create_table(self, table_name):
        # 여러문장일 때 따옴표 세개 써야 함
        ## test라는 이름의 테이블 생성
        ## 필드명 title을 text 자료형으로 생성
        ins_sql = 'create table ?(title text, pubd text, pus text, page integer, re integer)'
        self.cur.execute(ins_sql, table_name)

        # self.cur.execute('''
        # create table test2(
        # title text,
        # pubd text,
        # pus text,
        # page integer,
        # re integer
        # )''')

    def insert_data(self):

        self.cur.execute("insert into test values('개발자의 코드', '2016-05-26', 'a', 200, 0)")  # 정적 쿼리

        ins_sql = 'insert into test values(?,?,?,?,?)'  # 동적 쿼리. ?에 들어갈 내용을 모름
        self.cur.execute(ins_sql, ('클린코드', '2016-04-04', 'b', 300, 1))  # 동적 쿼리. ?에 들어갈 내용 지정

        books = [('한국사', '2016-02-02', 'c', 330, 1), ('물리개론', '2015-01-04', 'a', 130, 0),
                 ('건축학', '2013-10-14', 'e', 150, 0)]
        self.cur.executemany(ins_sql, books)  # 리스트로 여러개의 데이터를 한 번에 넣고 싶을 때 사용

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

    def delete_data(self):
        del_sql = 'delete from test where title=?'
        self.cur.execute(del_sql, ('중국사',))  # 튜플 형태

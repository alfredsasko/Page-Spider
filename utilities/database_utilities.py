import sqlite3 as lite


def create_database(database_path: str):
    conn = lite.connect(database_path)
    with conn:
        cur = conn.cursor()
        cur.execute('''
            DROP TABLE IF EXISTS words;
        ''')
        ddl = '''
            CREATE TABLE words (
                word text NOT NULL CONSTRAINT words_pk PRIMARY KEY,
                usage_count int DEFAULT 1
            );
        '''
        cur.execute(ddl)
        ddl = '''
        CREATE UNIQUE INDEX words_word_uindex
                ON words (word);
        '''
        cur.execute(ddl)
    conn.close()


def save_words_to_database(database_path: str, words_list: list):
    conn = lite.connect(database_path)
    with conn:
        cur = conn.cursor()
        for word in words_list:
            # check to see if the word is in there
            sql = f'''
                SELECT COUNT(word)
                FROM words
                WHERE word = '{word}';
            '''
            cur.execute(sql)
            count = cur.fetchone()[0]
            if count > 0:
                sql = f'''
                    UPDATE words
                    SET usage_count = usage_count + 1
                    WHERE word = '{word}'
                '''
            else:
                sql = f'''
                    INSERT INTO words (word)
                    VALUES ('{word}')
                '''
            cur.execute(sql)
        print("Database save complete!")

import pymysql


def insert(name, english, python, java):
    english = str(english)
    python = str(python)
    java = str(java)

    db = pymysql.connect(host = 'localhost', user = 'root', password = 'admin', database = 'stud_sys')
    cursor = db.cursor()
    sql = 'insert into stud_info (stud_name, english_score, python_score, java_score) values (' + "'" + name + "', " + english + ', ' + python + ', ' + java + ')'

    try:
        cursor.execute(sql)
        db.commit()
        return 0
    except Exception as e:
        db.rollback()
        print(e)
        return -1
    finally:
        db.close()




def searchAll():
    db = pymysql.connect(host = 'localhost', user = 'root', password = 'admin', database = 'stud_sys')
    cursor = db.cursor()
    sql = "select * from stud_info where stud_name not like '%delete%'"

    lst = []

    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        for row in results:
            info = {}
            info['id'] = row[0]
            info['name'] = row[1]
            info['english'] = row[2]
            info['python'] = row[3]
            info['java'] = row[4]
            lst.append(info)

        return lst
    except Exception as e:
        print(e)
        return -1
    finally:
        db.close()


def searchSingle(name):
    db = pymysql.connect(host = 'localhost', user = 'root', password = 'admin', database = 'stud_sys')
    cursor = db.cursor()
    sql = 'select * from stud_info where stud_name = ' + "'" + name + "'"

    try:
        cursor.execute(sql)
        result = cursor.fetchone()

        return result
    except Exception as e:
        print(e)
        return -1
    finally:
        db.close()


def update(name, infos):
    db = pymysql.connect(host = 'localhost', user = 'root', password = 'admin', database = 'stud_sys')
    cursor = db.cursor()
    sql = 'select * from stud_info where stud_name = ' + "'" + name + "'"

    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[1] == name:  # if user exist, do next
            categories = ['stud_name', 'english_score', 'python_score', 'java_score']
            s = ''
            i = 0

            for key, value in infos.items():
                if key in categories:
                    i += 1
                    s += key + " = " + str(value)
                    if i == len(infos):
                        break
                    s = s + ' , '
                else:
                    return -1
            sql = 'update stud_info set ' + s + ' where stud_name = ' + "'" + name + "'"
            # print(sql)
            # sql = 'update stud_info set ' + category + " = '" + value + "' where stud_name ='" + name + "'"
            cursor.execute(sql)
            db.commit()
            return 0
    except Exception as e:
        db.rollback()
        print(e)
        return -1
    finally:
        db.close()


def delete(name):
    db = pymysql.connect(host = 'localhost', user = 'root', password = 'admin', database = 'stud_sys')
    cursor = db.cursor()
    # sql = 'delete from stud_info where name =' + "'" + name + "'"
    delName = name + '_delete'

    sql = 'update stud_info set stud_name = ' + "'" + delName + "' where stud_name = " + "'" + name + "'"
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        return 0
    except:
        db.rollback()
        return -1
    finally:
        db.close()


# insert('heinz', 82, 83, 85)
# searchAll()
# searchSingle('tony')
# update('wangxiao', 'english_score', '80')

import os
import pymysql

db = pymysql.connect('localhost', 'root', '', 'rnn')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")


def deleteImg(id, path):  # 删除图片
    try:
        cursor.execute('DELETE FROM TAB_SLICE_IMG_INFO WHERE id = {id}'.format(id=id))
        db.commit()
        os.remove(path)
    except (ValueError, RuntimeError, FileNotFoundError):
        print('error save --> ', path)
        pass
    else:
        pass
    finally:
        pass


def main():
    cursor.execute('SELECT * FROM TAB_SLICE_IMG_INFO WHERE sign=0')
    # row = cursor.fetchone()
    # imgToData(row[1], row[2])
    # print(row)
    # return (row, 0)
    result = cursor.fetchall()
    for row in result:
        path = 'sliceImage/{distance}/{name}'.format(name=row[1], distance=row[2])
        print('delete-->', path)
        deleteImg(row[0], path)


if __name__ == "__main__":
    main()

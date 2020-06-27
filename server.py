import os
import sqlite3
db = 'data.db'

if os.path.isfile(db):
    try:
        conn = sqlite3.connect(db)

        c = conn.cursor()

        c.execute("UPDATE alarm SET finished_by_pult = 1 WHERE finished_by_pult = 0")

        c.execute('''
            INSERT INTO user_action (dict_action_type, action_data, action_data2, user_id, user_ip, time)
            SELECT 12, action_data, NULL, 0, "127.0.0.1", CAST((julianday("now") - 2440587.5) * 86400000.0 AS int)
            FROM (SELECT
            action_data, max(time) as time, dict_action_type, action_data2, user_id, user_ip, time
            FROM user_action
            WHERE dict_action_type IN (10, 11, 12 , 13, 20, 21, 22)
            GROUP BY action_data)
            WHERE dict_action_type <> 12
        ''')

        conn.commit()
        conn.close()
        print("All alarms in DB were completed!")
        k = input("Press enter to exit") 
    except:
        print ("Some error occurred!")
else:
    print ("Cannot find db file in current directory...")
    k = input("Press enter to exit") 
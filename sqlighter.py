import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT `id` FROM `subscriptions` WHERE `user_id` = ?', (user_id, )).fetchall()
            if (result == []):
                return 'net'
            else:
                return 'da'

    def add_subscriber(self, message, status = False):
        """Добавляем нового подписчика"""
        with self.connection:
            user_id = message.from_user.id
            user_first_name = message.from_user.first_name
            user_last_name = message.from_user.last_name
            username = message.from_user.username
            self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`, `user_first_name`, `user_last_name`, `username`) VALUES(?,?,?,?,?)", (user_id, status, user_first_name, user_last_name, username))




    def update_subscription(self, message, status, city = None, time = None):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            user_id = message.from_user.id
            if status == True:
                self.cursor.execute("UPDATE `subscriptions` SET `status` = 1 WHERE `user_id` = ?", (user_id, ))
                self.cursor.execute("UPDATE `subscriptions` SET `city` = ? WHERE `user_id` = ?", (city, user_id))
            elif status == False:
                self.cursor.execute("UPDATE `subscriptions` SET `status` = 0 WHERE `user_id` = ?", (user_id, ))
                self.cursor.execute("UPDATE `subscriptions` SET `city` = ? WHERE `user_id` = ?", (city, user_id))
                self.cursor.execute("UPDATE `subscriptions` SET `time` = ? WHERE `user_id` = ?", (time, user_id))

            first_name = str(self.cursor.execute("SELECT `user_first_name` FROM `subscriptions` WHERE `user_id` = ?", (user_id, )).fetchall()[0][0])

            if (first_name == 'None'):
                user_first_name = message.from_user.first_name
                user_last_name = message.from_user.last_name
                username = message.from_user.username
                self.cursor.execute("UPDATE `subscriptions` SET `user_first_name` = ? WHERE `user_id` = ?", (user_first_name, user_id))
                self.cursor.execute("UPDATE `subscriptions` SET `user_last_name` = ? WHERE `user_id` = ?", (user_last_name, user_id))
                self.cursor.execute("UPDATE `subscriptions` SET `username` = ? WHERE `user_id` = ?", (username, user_id))






    def subscription_status(self, user_id):
        """получаем статус подписки"""
        with self.connection:
            result = self.cursor.execute("SELECT `status` FROM `subscriptions` WHERE `user_id` = ?", (user_id, )).fetchall()
            if (result == [(0,)]):
                return False
            elif (result == [(1,)]):
                return True
            else:
                return result

    def subscription_city(self, user_id):
        """получаем город из подписки"""
        with self.connection:
            result = self.cursor.execute("SELECT `city` FROM `subscriptions` WHERE `user_id` = ?", (user_id, )).fetchall()
            return result

        """список всех пользователей"""
    def all_users(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `subscriptions`").fetchall()
            return(result)

        """получаем время из подписки"""
    def get_time(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time` FROM 'subscriptions' WHERE `user_id` = ?", (user_id, )).fetchall()
            return(result)

        """добавляем время"""
    def add_time(self, user_id, time):
        with self.connection:
            self.cursor.execute("UPDATE `subscriptions` SET `time` = ? WHERE `user_id` = ?", (time, user_id))



    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

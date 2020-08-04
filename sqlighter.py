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
            if (result != None):
                return True
            else:
                return False

    def add_subscriber(self, user_id, status = False):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)", (user_id, status))

    def update_subscription(self, user_id, status, city = None):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            if status == True:
                self.cursor.execute("UPDATE `subscriptions` SET `status` = 1 WHERE `user_id` = ?", (user_id, ))
                self.cursor.execute("UPDATE `subscriptions` SET `city` = ? WHERE `user_id` = ?", (city, user_id))
            elif status == False:
                self.cursor.execute("UPDATE `subscriptions` SET `status` = 0 WHERE `user_id` = ?", (user_id, ))
                self.cursor.execute("UPDATE `subscriptions` SET `city` = ? WHERE `user_id` = ?", (city, user_id))
            


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




    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
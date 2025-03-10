from flask_app.config.mySQLConnection import connectToMySQL
from flask import flash
from flask_app import DB
import math
import re
# import schedule
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
        
    
    
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.adminstration = data.get('adminstration', 'user')
        self.char_lvl = data.get('char_lvl', 1)
        self.location = data.get('location', "")
        self.about_me = data.get('about_me', "")
        self.interests = data.get('interests', "")
        self.exp = data['exp']
        self.HP = data.get('HP', 4)
        self.type = data.get('type')
        self.equipments = data.get('equipments', "")
        self.image = data.get('image', "")
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.is_active = data.get('is_active', 0)
        self.inv_items = data.get('inv_items', 'applehprevivebean')
        self.views = data.get('views', 0)
        self.pet = data.get('pet', 'none')
    @classmethod    
    def register(cls, data):
        query = "INSERT INTO users(username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        new_id = connectToMySQL(DB).query_db(query, data)
        
        return new_id
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL(DB).query_db(query)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        return all_users
    
    @classmethod
    def get_users_by_amount(cls,data):
        query = "SELECT * FROM users LIMIT %(limit)s OFFSET %(offset)s;"
        result = connectToMySQL(DB).query_db(query, data)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        return all_users
    @classmethod
    def get_latest_users_by_amount(cls,data):
        query = "SELECT * FROM users ORDER BY created_at DESC LIMIT %(limit)s OFFSET %(offset)s;"
        result = connectToMySQL(DB).query_db(query, data)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        return all_users
    
    @classmethod
    def get_latest_users_count(cls):
        query = "SELECT COUNT(*) FROM users WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY);"
        result = connectToMySQL(DB).query_db(query)
        return result[0]["COUNT(*)"]
    
    @classmethod
    def get_active_users(cls):
        query = "SELECT COUNT(*) FROM users WHERE adminstration = 'user' AND is_active = 1;"
        result = connectToMySQL(DB).query_db(query)
        print(result)
        return result[0]["COUNT(*)"]
    
    @classmethod
    def select_char(cls, data):
        query = """UPDATE users SET type = %(type)s where id = %(id)s"""
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def choose_inter(cls, data):
        query = """UPDATE users SET interests = %(interests)s where id = %(id)s"""
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_users_count(cls):
        query = "SELECT COUNT(*) FROM users;"
        result = connectToMySQL(DB).query_db(query)
        print(result[0]["COUNT(*)"])
        return result[0]["COUNT(*)"]
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return cls(result[0])
        return False
    
    @classmethod
    def get_one_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return False
        
    @classmethod
    def update(cls, data):
        query = """UPDATE users SET username = %(username)s, email = %(email)s, password = %(password)s,
                location = %(location)s, interests = %(interests)s WHERE id = %(id)s;"""
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def ban(cls, data):
        query = 'UPDATE users SET adminstration = "ban" WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def unban_demote(cls, data):
        query = 'UPDATE users SET adminstration = "user" WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def add_equipments(cls, data):
        query = 'UPDATE users SET equipments = %(equipment)s WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def depleat_HP(cls, data):
        query = 'UPDATE users SET HP = HP - 13 WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def add_HP(cls, data):
        query = 'UPDATE users SET HP = hp + 25 WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def max_HP(cls, data):
        query = 'UPDATE users SET HP = 100 WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def update_inv(cls, data):
        query = 'UPDATE users SET inv_items = %(inv_items)s WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    
    
    @classmethod
    def update_bio(cls,data) :
        query="UPDATE users SET about_me = %(about_me)s WHERE id = %(user_id)s ;"
        return connectToMySQL(DB).query_db(query, data)
    
    
    
    @classmethod
    def not_friends_users(cls, logged_in_user_id):
        query = """
        SELECT users.* 
        FROM users
        LEFT JOIN friends AS friendships_1 ON users.id = friendships_1.friend_id AND friendships_1.user_id = %(logged_in_user_id)s
        LEFT JOIN friends AS friendships_2 ON users.id = friendships_2.user_id AND friendships_2.friend_id = %(logged_in_user_id)s
        WHERE users.id != %(logged_in_user_id)s
        AND (friendships_1.friend_id IS NULL AND friendships_2.user_id IS NULL);
        """
        data = {'logged_in_user_id': logged_in_user_id}
        results = connectToMySQL(DB).query_db(query, data)
        users_not_friends = []
        for row in results:
            user_not_friend = cls(row)
            users_not_friends.append(user_not_friend)
        return users_not_friends
    
    @classmethod
    def add_pet(cls, data):
        query = 'UPDATE users SET pet = %(pet)s WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    
    @classmethod
    def reset_lvl(cls, data):
        query = 'UPDATE users SET char_lvl = 1 WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    
    @classmethod
    def reset_inv(cls, data):
        query = 'UPDATE users SET inv_items = "applehprevivebean" WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def reset_equipment(cls, data):
        query = 'UPDATE users SET equipments = "" WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def reset_pet(cls, data):
        query = 'UPDATE users SET pet = "none" WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "adminstration": self.adminstration,
            "char_lvl": self.char_lvl,
            "location": self.location,
            "about_me": self.about_me,
            "interests": self.interests,
            "exp": self.exp,
            "HP": self.HP,
            "type": self.type,
            "equipments": self.equipments,
            "image": self.image,
            "views": self.views or 0,
        }
    
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        if data['username'] == '':
            is_valid = False
            flash('Username should not be empty', 'username')
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Email not valid, try again", "email")
        if len(data['password']) < 8:
            is_valid = False
            flash("Password must contain at least 8 characters", "password")
        if data['password'] != data['confirm-password']:
            is_valid = False
            flash("Passwords must match", "confirm-password")
        return is_valid
    @classmethod
    def update_avatar(cls,data):
        query = 'UPDATE users SET image = %(image)s WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data)
    @classmethod
    def get_latest_users(cls,data:dict):
        query = "SELECT * FROM users WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) AND users.adminstration = 'user' ORDER BY created_at DESC LIMIT %(limit)s OFFSET %(offset)s;"
        result = connectToMySQL(DB).query_db(query,data)
        latest_users = [
            cls({**row, "created_at": row["created_at"].strftime("%Y-%m-%d")}) 
            for row in result
        ]
        return latest_users
    @classmethod
    def get_latest_users_by_amount(cls,data):
        query = "SELECT * FROM users WHERE users.adminstration = 'user' ORDER BY created_at DESC LIMIT %(limit)s OFFSET %(offset)s;"
        result = connectToMySQL(DB).query_db(query, data)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        return all_users
    @classmethod
    def get_users_grouped_by_day(cls):
        query = "SELECT DATE_FORMAT(created_at, '%Y-%m-%d') AS day, COUNT(*) as count FROM users WHERE users.adminstration = 'user' GROUP BY day ORDER BY day;"
        result = connectToMySQL(DB).query_db(query)
        return result
    @classmethod
    def get_latest_users_count_compared(cls) -> int:
        query = """SELECT COUNT(*) 
        FROM users 
        WHERE users.adminstration = 'user' 
        AND created_at BETWEEN DATE_SUB(NOW(), INTERVAL 14 DAY) AND DATE_SUB(NOW(), INTERVAL 7 DAY);"""
        result = connectToMySQL(DB).query_db(query)
        print(result[0]['COUNT(*)'])
        return result[0]['COUNT(*)']
    @classmethod
    def increment_view(cls,data):
        query = 'UPDATE users SET views = views + 1 WHERE id = %(id)s;'
        return connectToMySQL(DB).query_db(query, data) 
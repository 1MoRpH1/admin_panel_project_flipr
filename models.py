from app import mongo

# User model
class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        # Save user to the 'users' collection in MongoDB
        mongo.db.users.insert_one({
            'username': self.username,
            'email': self.email,
            'password': self.password
        })

# MongoDBInstance model
class MongoDBInstance:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def save(self):
        # Save MongoDB instance to the 'mongo_instances' collection in MongoDB
        mongo.db.mongo_instances.insert_one({
            'hostname': self.hostname,
            'port': self.port
        })

# Database model
class Database:
    def __init__(self, name):
        self.name = name

    def save(self):
        # Save database to the 'databases' collection in MongoDB
        mongo.db.databases.insert_one({
            'name': self.name
        })

# AccessRole model
class AccessRole:
    def __init__(self, name):
        self.name = name

    def save(self):
        # Save access role to the 'access_roles' collection in MongoDB
        mongo.db.access_roles.insert_one({
            'name': self.name
        })

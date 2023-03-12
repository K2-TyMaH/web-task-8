from pathlib import Path
import configparser

from mongoengine import connect


config = configparser.ConfigParser()
p = Path('/home/tymah/GoIT/web-task-8/RabbitMQ/mock/config.ini')
config.read(p)

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string
# mongodb+srv://tymah:<password>@mycluster.6ekshk8.mongodb.net/?retryWrites=true&w=majority

connection_string = f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"""
print(connection_string)
connect(host=connection_string, ssl=True)

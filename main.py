from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import text
from app import modelos
from app import dao
from app import config

def clear_database(engine):
    modelos.Base.metadata.drop_all(engine)
    modelos.Base.metadata.create_all(bind=engine)

def create_users(user_dao):
    # Create a new user
    try:
        user1 = user_dao.create_user('Armando', 'armando@ufpi.edu.br', 'armando')
        user2 = user_dao.create_user('Maria', 'maria@ufpi.edu.br', 'maria')
        user3 = user_dao.create_user('Carla', 'carla@ufpi.edu.br', 'carla')
    except Exception as ex: 
        print(f'Erro ao criar novo usuário: {str(ex)}')
    return user1, user2, user3

def list_users(user_dao):
    # Get all users
    all_users = user_dao.get_all_users()
    for usuario in all_users:
        print(usuario.username, usuario.email)

def update_user(user_dao, user_id, email):
    # Update user
    updated_user = user_dao.update_user(user_id, email)
    print(f"Dados atualizados do usuário {updated_user.username}: ")
    print(f"username: {updated_user.username}, e-mail: {updated_user.email}")

def delete_user(user_dao, user_id):
    # Delete user
    print(f"Remove o usuário {user_id}")
    user_dao.delete_user(user_id)

def select_all_users_by_SQL(engine):
    print("Lista todos os usuários cadastrados (usando SQL query): ")
    # Get all users using SQL Query
    sql_all_users = text("select * from users")
    conexao = engine.connect()

    with conexao as minha_conexao_banco:
        resultado = minha_conexao_banco.execute(sql_all_users)

        for registro in resultado:
            print(registro)    

print('Carrega configurações de banco de dados')
# Create database engine (database connection)
engine = create_engine(config.mysql_database_url)

# Create database session (a session to perform interation with database)
Session = sessionmaker(bind=engine)

# Declarative base for models
print("Limpa o banco de dados")
clear_database(engine)
print('Base de dados de produção carregada com sucesso!')

# Create a instance of session to interact with database
my_session = Session()

# create UserDAO to interact with table user via ORM
user_dao = dao.UserDAO(my_session)

user1, user2, user3 = create_users(user_dao)
print(f'Usuário {user1.username} criado com sucesso!')
print(f'Usuário {user2.username} criado com sucesso!')
print(f'Usuário {user3.username} criado com sucesso!')

print("Lista todos os usuários: ")
list_users(user_dao)

update_user(user_dao, user2.id, "novoemail@gmail.com")

delete_user(user_dao, user3.id)

select_all_users_by_SQL(engine)
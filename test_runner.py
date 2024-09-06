import unittest
from app.testes.suite_tc_userdao import UserDAOTest
from app.testes.suite_tc_notedao import NoteDAOTest
from sqlalchemy import create_engine
from app import config
from app import modelos
from HtmlTestRunner import HTMLTestRunner
import os

RESULTADOS_SUITE_TESTES_USUARIOS = "resultados/crud_users_suite"
RESULTADOS_SUITE_TESTES_NOTAS = "resultados/crud_notes_suite"
PATH_LOCAL = os.getcwd()

def set_test_suite(testcase):
    loader = unittest.TestLoader()
    test_suite = loader.loadTestsFromTestCase(testcase)
    return test_suite

def clean_database():
    # Create database engine
    engine = create_engine(config.mysql_database_url)
    # Clean database
    print("Limpa o banco de dados")
    modelos.Base.metadata.drop_all(engine)
    modelos.Base.metadata.create_all(bind=engine)

print("Executa a suite de testes de CRUD de Usuários")
my_suite_users = set_test_suite(testcase=UserDAOTest)
runner_users = HTMLTestRunner(output=RESULTADOS_SUITE_TESTES_USUARIOS)
runner_users.run(my_suite_users)
print()

clean_database()

print("Executa a suite de testes de CRUD de Notas de um usuário")
my_suite_notes = set_test_suite(testcase=NoteDAOTest)
runner_notes = HTMLTestRunner(output=RESULTADOS_SUITE_TESTES_NOTAS)
runner_notes.run(my_suite_notes)
print()

print(f"O resultado dos testes estão disponíveis em: ")
print(f"{PATH_LOCAL}/{RESULTADOS_SUITE_TESTES_USUARIOS}")
print(f"{PATH_LOCAL}/{RESULTADOS_SUITE_TESTES_NOTAS}")
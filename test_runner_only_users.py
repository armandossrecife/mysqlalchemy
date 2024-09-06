import unittest
from app.testes.suite_tc_userdao import UserDAOTest

# Suite de testes em modo texto

def suite_users():
    loader = unittest.TestLoader()
    test_suite = loader.loadTestsFromTestCase(UserDAOTest)
    return test_suite

my_suite_users = suite_users()

print("Executa a suite de testes de Usuários")
runner_users = unittest.TextTestRunner()
resultados_testes_users = runner_users.run(my_suite_users)
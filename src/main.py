"""
CLI program to get the movements in a Ruralvia account.
"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from argparse import Namespace, ArgumentParser
from src.ruralvia import Login

# Constants
DEBUG = False
FILES = [ "cuentas.xlsx" ]

# Function definitions

def get_arguments() -> Namespace:
    """
    Function to parse the arguments passed by CLI
    
    returns: argparse.Namespace with the parsed arguments
    """
    parser = ArgumentParser(
        description="Programa para descargarse los movimientos de Ruralvia")
    
    parser.add_argument("-u", "--user", 
                        required=True, 
                        help="Usuario con el que iniciar sesión en Ruralvia")
    
    return parser.parse_args()

def main() -> None:
    args = get_arguments()
    
    # Get the Excel file from the Ruralvia site

    edge_options = Options()
    edge_options.add_experimental_option("detach", DEBUG)
    driver = webdriver.Edge(options=edge_options)

    current_pg = Login(driver)
    current_pg = current_pg.do_login(args.user)
    
    for account in current_pg.get_accounts():
        account_pg = current_pg.nav_account(account) 
        account_pg.download()
        account_pg.back()

# Allons'y!

if __name__ == "__main__":
    main()
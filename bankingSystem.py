import textwrap

# Constantes
LIMITE_SAQUES = 3
AGENCIA = "0001"

# Funções de interação com o usuário
def menu():
    """Exibe o menu de opções para o usuário e retorna a opção selecionada."""
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def get_user_input(prompt, validator=None):
    """Solicita a entrada do usuário e retorna o valor, com validação opcional."""
    while True:
        user_input = input(prompt)
        if validator and not validator(user_input):
            print("\n@@@ Entrada inválida, tente novamente. @@@")
            continue
        return user_input

def is_valid_cpf(cpf):
    """Verifica se o CPF informado é válido."""
    # Implementar lógica de validação de CPF aqui
    return len(cpf) == 11 and cpf.isdigit()

def is_valid_date(date_str):
    """Verifica se a data de nascimento informada está no formato correto."""
    # Implementar lógica de validação de data aqui
    return len(date_str.split("-")) == 3

# Funções de lógica de negócio
def deposit(balance, amount, statement):
    """Realiza o depósito, atualizando o saldo e o extrato."""
    if amount > 0:
        balance += amount
        statement += f"Depósito:\tR$ {amount:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return balance, statement

def withdraw(balance, amount, statement, limit, num_withdrawals, max_withdrawals):
    """Realiza o saque, verificando se o valor é válido e se não excede o saldo, limite ou número máximo de saques."""
    exceeds_balance = amount > balance
    exceeds_limit = amount > limit
    exceeds_withdrawals = num_withdrawals >= max_withdrawals

    if exceeds_balance:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif exceeds_limit:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif exceeds_withdrawals:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif amount > 0:
        balance -= amount
        statement += f"Saque:\t\tR$ {amount:.2f}\n"
        num_withdrawals += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return balance, statement, num_withdrawals

def display_statement(balance, statement):
    """Exibe o extrato com o saldo atual."""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not statement else statement)
    print(f"\nSaldo:\t\tR$ {balance:.2f}")
    print("==========================================")

def create_user(users):
    """Cria um novo usuário e adiciona-o à lista de usuários."""
    cpf = get_user_input("Informe o CPF (somente número): ", is_valid_cpf)
    user = next((u for u in users if u["cpf"] == cpf), None)

    if user:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    name = input("Informe o nome completo: ")
    birth_date = get_user_input("Informe a data de nascimento (dd-mm-aaaa): ", is_valid_date)
    address = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    users.append({"name": name, "birth_date": birth_date, "cpf": cpf, "address": address})
    print("=== Usuário criado com sucesso! ===")

def create_account(agency, account_number, users):
    """Cria uma nova conta, associando-a a um usuário existente."""
    cpf = get_user_input("Informe o CPF do usuário: ", is_valid_cpf)
    user = next((u for u in users if u["cpf"] == cpf), None)

    if user:
        print("\n=== Conta criada com sucesso! ===")
        return {"agency": agency, "account_number": account_number, "user": user}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def list_accounts(accounts):
    """Exibe a lista de contas com seus respectivos detalhes."""
    for account in accounts:
        line = f"""\
            Agência:\t{account['agency']}
            C/C:\t\t{account['account_number']}
            Titular:\t{account['user']['name']}
        """
        print("=" * 100)
        print(textwrap.dedent(line))

# Função principal
def main():
    balance = 0
    limit = 500
    statement = ""
    num_withdrawals = 0
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            amount = float(get_user_input("Informe o valor do depósito: "))
            balance, statement = deposit(balance, amount, statement)

        elif option == "s":
            amount = float(get_user_input("Informe o valor do saque: "))
            balance, statement, num_withdrawals = withdraw(
                balance, amount, statement, limit, num_withdrawals, LIMITE_SAQUES
            )

        elif option == "e":
            display_statement(balance, statement)

        elif option == "nu":
            create_user(users)

        elif option == "nc":
            account_number = len(accounts) + 1
            account = create_account(AGENCIA, account_number, users)
            if account:
                accounts.append(account)

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()

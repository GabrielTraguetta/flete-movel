"""
===============================================================================
MODEL — camada de DADOS e REGRAS DE NEGÓCIO (padrão MVC)
===============================================================================
Este é o ÚNICO arquivo de Model do projeto. Ele reúne:

    1) As classes que representam os DADOS do app (Transaction e Contact);
    2) A classe principal do Model — `BankAccount` — que guarda o estado da
       conta (saldo, extrato, contatos) e concentra TODAS as regras de
       negócio (ex.: "não pode transferir valor <= 0", "saldo não pode
       ficar negativo"). Nem a View nem o Controller sabem esses detalhes;
       eles só chamam os métodos que o Model oferece.

O Model NUNCA importa `flet` e NUNCA sabe desenhar nada na tela. Ele só
guarda e manipula dados. Quem desenha é a View; quem decide "quando" chamar
o quê é o Controller.

"""

"""
=============================================================================
MODEL — camada de DADOS e REGRAS DE NEGÓCIO (padrão MVC)
=============================================================================
Classes deste arquivo:
    Transaction  -> uma linha do extrato
    Contact      -> uma pessoa para quem se pode fazer Pix
    Account      -> conta básica (titular + saldo)
    BankAccount  -> conta do app: estado (bloqueio, saldo visível), contatos,
                    extrato e regras (transferir, alternar visibilidade...)

O Model NÃO conhece o Flet: não desenha nada e não sabe de telas.
"""
from dataclasses import dataclass, field
from datetime import datetime


def format_money(value: float) -> str:
    """Formata como moeda brasileira: 1234.5 -> 'R$ 1.234,50'."""
    texto = f"{abs(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    sinal = "-" if value < 0 else ""
    return f"{sinal}R$ {texto}"


@dataclass
class Transaction:
    """Uma linha do extrato. `amount` negativo = saída, positivo = entrada."""
    description: str
    amount: float
    date: str


@dataclass
class Contact:
    """Pessoa para quem é possível fazer um Pix."""
    name: str
    key: str  # chave Pix (cpf, e-mail, telefone...)


class Account:
    """Conta básica: titular e saldo."""

    def __init__(self, holder: str, balance: float = 0.0):
        self.holder = holder
        self.balance = balance

    @property
    def balance_text(self) -> str:
        return format_money(self.balance)


class BankAccount(Account):
    """Conta do Noobank, com todo o estado e as regras do app."""

    def __init__(self, holder: str, balance: float = 0.0):
        super().__init__(holder, balance)
        self.unlocked: bool = False          # o app começa bloqueado
        self.balance_visible: bool = True
        self.contacts: list[Contact] = []
        self.transactions: list[Transaction] = []

    # ---------------- Início ----------------
    def toggle_balance_visibility(self) -> None:
        self.balance_visible = not self.balance_visible

    @property
    def balance_text(self) -> str:
        """Saldo pronto para exibir (ou escondido)."""
        return format_money(self.balance) if self.balance_visible else "R$ ••••••"

    # ---------------- Pix ----------------
    def transfer(self, contact_name: str, amount: float) -> None:
        """
        Efetiva um Pix. Levanta ValueError (com a mensagem pronta para
        mostrar ao usuário) se a regra de negócio não for respeitada.
        """
        if amount <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        if amount > self.balance:
            raise ValueError("Saldo insuficiente.")

        self.balance -= amount
        self.transactions.append(
            Transaction(
                f"Pix para {contact_name}",
                -amount,
                datetime.now().strftime("%d/%m/%Y"),
            )
        )


def create_default_account() -> BankAccount:
    """Cria a conta fictícia já populada com os dados iniciais."""
    account = BankAccount("Dev", 1500.00)
    account.contacts = [
        Contact("Ana Souza", "ana@email.com"),
        Contact("Bruno Lima", "(15) 99999-1111"),
        Contact("Carla Mendes", "123.456.789-00"),
    ]
    account.transactions = [
        Transaction("Salário", 2500.00, "25/09/2026"),
        Transaction("Mercado", -320.50, "27/09/2026"),
        Transaction("Pix para Bruno Lima", -80.00, "28/09/2026"),
        Transaction("Transferência recebida", 150.00, "29/09/2026"),
    ]
    return account
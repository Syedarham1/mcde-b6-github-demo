import uuid

class TransactionRecord:
    def __init__(self, action, amount, resulting_balance):
        self._tx_id = str(uuid.uuid4())
        self._action = action
        self._amount = amount
        self._resulting_balance = resulting_balance

    @property
    def tx_id(self): return self._tx_id
    @property
    def action(self): return self._action
    @property
    def amount(self): return self._amount
    @property
    def resulting_balance(self): return self._resulting_balance

class Account:
    def __init__(self, account_id, initial_balance=0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self._account_id = account_id
        self._balance = float(initial_balance)
        self._transactions = []

    @property
    def account_id(self): return self._account_id
    @property
    def balance(self): return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self._transactions.append(TransactionRecord("DEPOSIT", amount, self._balance))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        self._transactions.append(TransactionRecord("WITHDRAW", amount, self._balance))

    @property
    def statement(self):
        return [
            {"tx_id": t.tx_id, "action": t.action, "amount": t.amount, "balance": t.resulting_balance}
            for t in self._transactions
        ]

class Bank:
    def __init__(self):
        self._accounts = {}

    def create_account(self, account_id, initial_balance=0.0):
        if account_id in self._accounts:
            raise ValueError("Account ID already exists.")
        self._accounts[account_id] = Account(account_id, initial_balance)
        return self._accounts[account_id]

    def get_account(self, account_id):
        if account_id not in self._accounts:
            raise ValueError("Account does not exist.")
        return self._accounts[account_id]

    def transfer(self, from_id, to_id, amount):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        acc_from = self.get_account(from_id)
        acc_to = self.get_account(to_id)

        if acc_from.balance < amount:
            raise ValueError("Insufficient funds for atomic transfer.")

        # Atomic execution
        acc_from.withdraw(amount)
        try:
            acc_to.deposit(amount)
        except Exception as e:
            # Rollback withdrawal if deposit fails
            acc_from.deposit(amount)
            raise RuntimeError(f"Transfer failed and rolled back: {e}")

if __name__ == "__main__":
    bank = Bank()
    a = bank.create_account("A", 1000)
    b = bank.create_account("B", 200)
    bank.transfer("A", "B", 350)
    print(f"A={a.balance}, B={b.balance}")  
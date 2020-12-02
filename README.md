# krip_funcs
Custom functions created by kripaar (kv_HK)
___
# sqlite.py
* The `database` and `table` objects are inside for now  
### Quick Example
```py
from kripfunc.sqlite import database

db = database()  # Leave parameter blank => storing everything in ram, not opening any file

table = db.create_table("credit_card", {"card_number": "INT NON NULL", "expire": "TEXT", "CVC": "CHAR(3)"})

table.append(1234567890123456, "07/21", "051")
table.append_many((2345678901234567, "08/31", "028"), (3456789012345678, "10/01", "777"))

print(table.get())   # (1234567890123456, '07/21', '051')
print(table.get(0))  # [(1234567890123456, '07/21', '051'), (2345678901234567, '08/31', '028'), (3456789012345678, '10/01', '777')]
print(table.get(2))  # [(1234567890123456, '07/21', '051'), (2345678901234567, '08/31', '028')]
```

# commander.py
* Convert a command-line form of string into running your commands
### Quick Example
```py
from kripfunc.commander import Commander

cmd = Commander("/")

@cmd(name="money")
def bank():
    print("You have no balance in your bank account")

@cmd(parent="money")
def top():
    print("The top is Li Ka Shing")

@cmd(name="give", parent="money")
def i_had_loan_from(account_payable, amount_to_give):
    print(f"You've given ${amount_to_give} to {account_payable}")


c.run("/money")                               # You have no balance in your bank account
c.run("/money top")                           # The top is Li Ka Shing
c.run("/money give \"Kripaar Bank\" 1000")    # You've given $1000 to Kripaar Bank
```

```py
from kripfunc.commander import Commander

cmd = Commander("Hey, ")

@cmd(name="what")
def a():
    print("What?")


@cmd(name="is", parent="what")
def b():
    print("Hello?")


@cmd(parent="what:is")
def going():
    print("Are you saying?")


@cmd(name="on?", parent="what:is:going")
def on():
    print("You meant \"What's going on?\"? There's nothing weird going on!")


c.run("Hey, what")                  # What?
c.run("Hey, what is going on?")     # You meant "What's going on?"? There's nothing weird going on!
```
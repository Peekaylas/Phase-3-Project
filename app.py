import click
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Account, Category, Transaction, User
from datetime import datetime

engine = create_engine("sqlite:///pocket_money_tracker.db")
session = Session(bind=engine)

def validate_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return (str(date_obj.year), str(date_obj.month).zfill(2), str(date_obj.day).zfill(2))
    except ValueError:
        raise click.BadParameter("Date must be in YYYY-MM-DD format (e.g., 2025-05-26)")

def validate_amount(amount_str):
    try:
        return float(amount_str)
    except ValueError:
        raise click.BadParameter("Amount must be a number (e.g., 10.50 or -5.00)")

@click.group()
def cli():
    pass

@cli.command()
@click.argument("username")
def add_user(username):
    click.echo(f"Debug: Received username = {username}")  # Debug print
    if username is None:
        raise click.BadParameter("Username cannot be None")
    user = User(username=username)
    session.add(user)
    session.commit()
    click.echo(f"Added user: {username} (ID: {user.id})")

@cli.command()
@click.argument("user_id", type=int)
@click.argument("name")
def add_account(user_id, name):
    user = session.query(User).get(user_id)
    if not user:
        click.echo(f"User ID {user_id} not found.")
        return
    account = Account(name=name, user_id=user_id)
    session.add(account)
    session.commit()
    click.echo(f"Added account: {name} (ID: {account.id})")

@cli.command()
@click.argument("name")
def add_category(name):
    category = Category(name=name)
    session.add(category)
    session.commit()
    click.echo(f"Added category: {name} (ID: {category.id})")

@cli.command()
@click.argument("account_id", type=int)
@click.argument("amount", type=validate_amount)
@click.argument("category_id", type=int)
@click.argument("date")
@click.argument("description")
def add_transaction(account_id, amount, category_id, date, description):
    date_tuple = validate_date(date)
    date_str = "-".join(date_tuple)
    account = session.query(Account).get(account_id)
    category = session.query(Category).get(category_id)
    if not account or not category:
        click.echo(f"Account ID {account_id} or Category ID {category_id} not found.")
        return
    transaction = Transaction(amount=amount, date=date_str, description=description, account_id=account_id)
    transaction.categories.append(category)
    session.add(transaction)
    account.balance += amount
    session.commit()
    details = {"ID": transaction.id, "Amount": transaction.amount, "Date": transaction.date, "Description": transaction.description, "Account": account.name, "Category": category.name}
    click.echo("Added transaction:")
    for k, v in details.items():
        click.echo(f"{k}: {v}")

@cli.command()
@click.argument("account_id", type=int)
def list_transactions(account_id):
    account = session.query(Account).get(account_id)
    if not account:
        click.echo(f"Account ID {account_id} not found.")
        return
    transactions = account.transactions
    if not transactions:
        click.echo("No transactions found for this account.")
        return
    click.echo(f"Transactions for {account.name}:")
    for t in transactions:
        category_names = [c.name for c in t.categories]
        click.echo(f"ID: {t.id}, Amount: {t.amount}, Date: {t.date}, Description: {t.description}, Categories: {', '.join(category_names)}")

@cli.command()
@click.argument("username")
def add_user(username):
    click.echo(f"Debug: Received username = {username}")
    if username is None:
        raise click.BadParameter("Username cannot be None")
    click.echo("Debug: Creating User object")
    user = User(username=username)
    click.echo(f"Debug: User object created: {user}")
    click.echo("Debug: Adding user to session")
    session.add(user)
    click.echo("Debug: Committing session")
    session.commit()
    click.echo(f"Added user: {username} (ID: {user.id})")

if __name__ == "__main__":
    try:
        cli()
    finally:
        session.close()
"""Database sqlitedatabase.py

This file contains the SQLiteDatabase Class
"""

import sqlite3

from discord import Member
from .abstract import Database

class SQLiteDatabase(Database):
    """SQLite Database

    This class is a wrapper for SQLite
    """

    def __init__(self, filename="database"):

        self.database = sqlite3.connect(f"{filename}.database")

        cursor = self.database.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INT,
            balance INT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS investments (
            id INT,
            investment INT,
            maturing_date TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS roblox_link (
            id INT,
            roblox_id INT
        )
        """)
        self.database.commit()

    #######
    # GET #
    #######
    def get_member_balance(self, member: Member) -> int:
        cursor = self.database.cursor()
        response = cursor.execute("SELECT balance FROM accounts WHERE id=?", (member.id,))
        if not response:
            self.create_account(member)
            return 0
        return response[0]


    ########
    # POST #
    ########
    def create_account(self, member: Member, initial_balance=0) -> None:
        cursor = self.database.cursor()
        response = cursor.execute("SELECT balance FROM accounts WHERE id=?", (member.id,))
        if not response:
            cursor.execute("UPDATE accounts set balance=? WHERE id=?", (initial_balance, member.id))
        else:
            cursor.execute("INSERT INTO accounts VALUES (?, ?)", (member.id, initial_balance))
        self.database.commit()

    ##########
    # Update #
    ##########
    def transfer_funds(self, sender: Member, receiver: Member, amount: int) -> None:
        cursor = self.database.cursor()
        cursor.execute("UPDATE accounts SET balance=balance-? WHERE id=?", (amount, sender.id))
        if self.get_member_balance(receiver) >= 0:
            cursor.execute("UPDATE accounts SET balance=balance+? WHERE id=?", (amount, sender.id))
        else:
            self.create_account(receiver, initial_balance=amount)
        self.database.commit()


    def add_funds(self, member: Member, amount: int) -> None:
        cursor = self.database.cursor()
        if self.get_member_balance(member) >= 0:
            cursor.execute("UPDATE accounts SET balance=balance+? WHERE id=?", (amount, member.id))
        else:
            self.create_account(member, initial_balance=amount)
        self.database.commit()

    def remove_funds(self, member: Member, amount: int) -> None:
        cursor = self.database.cursor()
        if self.get_member_balance(member) >= amount:
            cursor.execute("UPDATE accounts SET balance=balance-? WHERE id=?", (amount, member.id))
        else:
            return Exception
        self.database.commit()
        
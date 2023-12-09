"""Database Abstract.py

This file contains the Abstract classes that ALL 
DATABASE CLASSES EXTENDING MUST FOLLOW
in case other classes are needed
"""

from abc import ABC, abstractmethod
from typing import (
    List,
    Tuple
)

from discord import Member
import datetime
from skills_sorter import Team
class Database(ABC):
    """
    Abstract Synchronous Database Class.
    """

    #######
    # GET #
    #######
    @abstractmethod
    def get_team_data(self, id:int) -> int:
        """Get team dataa

        Retrieve data of a member
        """


    ##########
    # Update #
    ##########
    @abstractmethod
    def update_entry(self, team:Team ) -> bool:
        """Update Entry

        Updates the entry of a team
        """

    @abstractmethod
    def add_funds(self, member: Member, amount: int) -> None:
        """Add Funds

        Add funds to a members.
        """

    @abstractmethod
    def remove_funds(self, member: Member, amount: int) -> None:
        """Remove Funds

        Remove funds to a members.
        """

class AsyncDatabase(ABC):
    """
    Abstract Asynchronous Database Class
    """

    @abstractmethod
    async def connect(self) -> None:
        """Initialize the Database Connection."""

    @abstractmethod
    async def close(self) -> None:
        """Close the Database Connection."""


    #######
    # GET #
    #######
    @abstractmethod
    async def get_member_balance(self, member: Member) -> int:
        """Get member Balance

        Retrieve the balance of a member.
        """

    @abstractmethod
    async def get_investment_amount(self, member: Member) -> int:
        """Get Investment Amount

        Return the total amount invested by a user.
        """

    @abstractmethod
    async def get_item_names(self) -> List[str]:
        """Get Item Names

        Return the names of every item in the database.
        """

    @abstractmethod
    async def get_item(self, name: str) -> Tuple[str, str, str, int]:
        """Get Item

        Return the information about the specified Item.
        """

    @abstractmethod
    async def get_investments(self, member: Member) -> List[Tuple[int, int, str]]:
        """Get Investments

        This will return all the investments of the user.
        """

    @abstractmethod
    async def get_all_investments(self) -> List[Tuple[int, int, int, str]]:
        """Get All Investments

        Return every single investment stored.
        """

    @abstractmethod
    async def get_investment_bracket(self, number: int) -> Tuple[int, int, float]:
        """Get Investment Bracket

        Given the number return the minimum value for investments,
        maximum value for investments,
        and interest rate.

        """

    @abstractmethod
    async def get_roblox_id(self, member: Member) -> int:
        """Get Roblox ID
        
        Get Someones Roblox ID.
        """

    ##########
    # Update #
    ##########
    @abstractmethod
    async def transfer_funds(self, sender: Member, receiver: Member, amount: int) -> None:
        """Transfer Funds

        Transfers funds from one account to another.
        """

    @abstractmethod
    async def add_funds(self, member: Member, amount: int) -> None:
        """Add Funds

        Add funds to a members.
        """

    @abstractmethod
    async def remove_funds(self, member: Member, amount: int) -> None:
        """Remove Funds

        Remove funds to a members.
        """

    ##########
    # DELETE #
    ##########

    @abstractmethod
    async def cancel_investment(self, member: Member, amount: int, date: str) -> None:
        """Cancel Investments
        """

    @abstractmethod
    async def finish_investment(self, member: Member, amount: int, profit: int, date: str) -> None:
        """Finish Investments
        """
        
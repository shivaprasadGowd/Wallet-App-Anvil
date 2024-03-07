from ._anvil_designer import transaction_historyTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class transaction_history(transaction_historyTemplate):
  def __init__(self, user=None, **properties):
    self.user = user
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    item= app_tables.transactions.search(user=self.user['username'])
    self.repeating_panel_1.items= item

    # Any code you write here will run before the form opens.

 

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("deposit",user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("transfer",user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("withdraw",user=self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("service",user=self.user)

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Home")

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("service",user=self.user)

  def button_3_click(self, **event_args):
    open_form('transfer')

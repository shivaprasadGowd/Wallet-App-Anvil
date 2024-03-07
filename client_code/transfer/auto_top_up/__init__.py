from ._anvil_designer import auto_top_upTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class auto_top_up(auto_top_upTemplate):
  def __init__(self, user=None, **properties):
    self.user = user
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_account_numbers = anvil.server.call('get_user_account_numbers', self.user['username'])
    self.dropdown_account_numbers.items = user_account_numbers
    if self.user['top_up']== True:
      self.button_1.visible= False
    else:
      self.button_2.visible= False




  def button_1_click(self, **event_args):
    acc = self.dropdown_account_numbers.selected_value
    wallet3 = anvil.server.call('generate_unique_id', self.user['username'], self.user['phone'])
    self.user['top_up']= True
    self.user.update()
    self.button_1.visible = False
    self.button_2.visible = True
    if self.user['top_up'] is not None and self.user['top_up']== True:
      for_emoney = anvil.server.call('get_accounts_emoney_with_user',self.user['username'])
      money_in_emoney= for_emoney['e_money']
      threshold =2000
      print("hello")
      if float(money_in_emoney)< threshold:
        final= str(float(money_in_emoney) + 5000)
        print("hi there")
        if self.validate()== True:
          print("hi I'm sending user value")
          self.deduct_currencies(final)
          anvil.server.call('update_all_rows',self.user['username'], final)

          # Record successful automatic transaction and currency deduction
          self.record_transaction("Automatic Top-Up", f"₹5000", "success")
          
          self.button_1.visible = False
          self.button_2.visible = True
        else:
          self.label_5.text = "Insufficient Funds put money in your casa account"
          # Record failed transaction due to insufficient funds
          self.record_transaction("Automatic Top-Up", f"₹5000", "failed")
      else:
        return f"E-wallet balance ({money_in_emoney}) is above the threshold. No top-up needed."
    
  def validate(self):
    acc= self.dropdown_account_numbers.selected_value
    currencies_table = app_tables.currencies.get(casa=int(acc))
    conversion_usd = float(currencies_table['money_usd'])*80
    conversion_euro = float(currencies_table['money_euro'])*85
    conversion_swis = float(currencies_table['money_swis']) * 90
    conversion_inr = float(currencies_table['money_inr']) * 1
    if conversion_usd > 5000:
        return True
    elif conversion_euro  > 5000:
        return True
    elif conversion_swis > 5000:
        return True
    elif conversion_inr > 5000:
        return True
    else:
        return False
  
  def deduct_currencies(self, amount):
    acc= self.dropdown_account_numbers.selected_value
    currencies_table = app_tables.currencies.get(casa=int(acc))
    conversion_usd = float(currencies_table['money_usd'])*80
    conversion_euro = float(currencies_table['money_euro'])*85
    conversion_swis = float(currencies_table['money_swis']) * 90
    conversion_inr = float(currencies_table['money_inr']) * 1 
    if conversion_usd > 5000:
        currencies_table['money_usd'] = str((conversion_usd- 5000)/80)
        currencies_table.update()
        # Record successful deduction in the transactions table
        self.record_transaction("Currency Deducted", "$-USD", "success")
    elif conversion_euro  > 5000:
        currencies_table['money_euro'] = str((conversion_euro- 5000)/85)
        currencies_table.update()
        # Record successful deduction in the transactions table
        self.record_transaction("Currency Deducted", "Є-EURO", "success")
    elif conversion_swis > 5000:
        currencies_table['money_swis'] = str((conversion_swis - 5000) / 90)
        currencies_table.update()
        # Record successful deduction in the transactions table
        self.record_transaction("Currency Deducted", "₣-SWIS", "success")
    elif conversion_inr > 5000:
        currencies_table['money_inr'] = str((conversion_inr - 5000) / 1)
        currencies_table.update()
        # Record successful deduction in the transactions table
        self.record_transaction("Currency Deducted", "₹-INR", "success")
    else:
      self.label_5.text = "Insufficient funds"
      # Record failed deduction in the transactions table
      self.record_transaction("Currency Deduction", "Unknown", "failed")

  def record_transaction(self, transaction_type, details, proof):
        current_datetime = datetime.now()
        acc = self.dropdown_account_numbers.selected_value
        wallet3 = anvil.server.call('generate_unique_id', self.user['username'], self.user['phone'])
        app_tables.transactions.add_row(
            user=self.user['username'],
            casa = int(acc),
            e_wallet=wallet3, 
            money=details,
            date=current_datetime,
            transaction_type=transaction_type,
            proof=proof
        )
        


  def button_2_click(self, **event_args):
    self.user['top_up']= False
    self.user.update()
    self.button_1.visible = True
    self.button_2.visible = False

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("service",user=self.user)

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

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer",user=self.user)

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Home")

  def button_3_click(self, **event_args):
    open_form('transfer')

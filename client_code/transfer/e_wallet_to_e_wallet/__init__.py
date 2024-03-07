from ._anvil_designer import e_wallet_to_e_walletTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class e_wallet_to_e_wallet(e_wallet_to_e_walletTemplate):
  
    def __init__(self, user=None, **properties):
        self.user = user
        self.init_components(**properties)
        self.label_1.text = f"Welcome to Green Gate Financial, {user['username']}"


    def button_1_click(self, **event_args):
        current_datetime = datetime.now()
        depoitor = self.text_box_1.text
        wallet_id = self.text_box_2.text
        transfer_amount = self.text_box_3.text
        
        depositor_wallet_id= anvil.server.call('generate_unique_id', self.user['username'], self.user['phone'])
        #getting the depositor's details
        fore_money_depositor = anvil.server.call('get_accounts_emoney_using_wallet_id', depositor_wallet_id)
        #getting the reciever's details
        fore_money_sent = anvil.server.call('get_accounts_emoney_using_wallet_id',wallet_id)
        recieve = float(fore_money_sent['e_money']) if fore_money_sent['e_money'] else 0
        # if(fore_money_sent['e_money']== None):
        #   anvil.server.call('update_rows_emoney_trasaction',wallet_id, str(0))
        if (transfer_amount < 5) or (transfer_amount > 50000):
           proof="failed"
           self.label_4.text = "Transfer amount should be between 5 and 50000 for a transfer Funds." 
           app_tables.transactions.add_row(
            user=self.user['username'],
            e_wallet=f"{depositor_wallet_id} to {wallet_id}",
            money=f"₹-{transfer_amount}",
            date=current_datetime,
            transaction_type="E-wallet to E-wallet",
            proof=proof
           )        
        else:
           if float(fore_money_depositor['e_money']) < transfer_amount:
             proof = "failed"
             self.label_4.text = "Insufficient Funds in E-Wallet."
             app_tables.transactions.add_row(
                user=self.user['username'],
                e_wallet=f"{depositor_wallet_id} to {wallet_id}",
                money=f"₹-{transfer_amount}",
                date=current_datetime,
                transaction_type="E-wallet to E-wallet",
                proof=proof
             )
           else: 
             proof="success"
             #calculating the money to be added in the recieve's end
             transfer_fianl_sent_amount= recieve + transfer_amount
             #calculating the money to be deducted in the depositor's end
             transfer_amount_final = float(fore_money_depositor['e_money'])-transfer_amount
             #setting the value
             anvil.server.call('update_rows_emoney_trasaction',depositor_wallet_id, str(transfer_amount_final))
             anvil.server.call('update_rows_emoney_trasaction',wallet_id, str(transfer_fianl_sent_amount))
             #Updating the daily limit
             answer = float(self.user['limit'])- transfer_amount
             anvil.server.call('update_daily_limit', self.user['username'], str(answer))
             self.label_4.text = "Money transferred successfully"

             app_tables.transactions.add_row(
                 user=self.user['username'],
                 e_wallet=f"{depositor_wallet_id} to {wallet_id}",
                 money=f"₹-{transfer_amount}",
                 date=current_datetime,
                 transaction_type="E-wallet to E-wallet",
                 proof=proof
               )
        if self.user['top_up'] is not None and self.user['top_up']== True:
          for_emoney = anvil.server.call('get_accounts_emoney_with_user',self.user['username'])
          money_in_emoney= for_emoney['e_money']
          threshold =2000
          if float(money_in_emoney)< threshold:
            final= str(float(money_in_emoney) + 5000)
            print("hi there")
            if self.validate()== True:
              print("hi I'm sending user value")
              self.deduct_currencies(final)
              anvil.server.call('update_all_rows',self.user['username'], final)
            else:
              self.label_4.text = "Insufficient Funds put money in your casa account"
          else:
            return f"E-wallet balance ({money_in_emoney}) is above the threshold. No top-up needed."
            
          
    def validate(self):
      currencies_table = app_tables.currencies.search(user=self.user['username'])
      for row in currencies_table:
         conversion_usd = float(row['money_usd'] if 'money_usd' in row else 0) * 80
         conversion_euro = float(row['money_euro'] if 'money_euro' in row else 0) * 85
         conversion_swis = float(row['money_swis'] if 'money_swis' in row else 0) * 90
         conversion_inr = float(row['money_inr'] if 'money_inr' in row else 0) * 1
         # conversion_usd = float(currencies_table['money_usd'])*80
         # conversion_euro = float(currencies_table['money_euro'])*85
         # conversion_swis = float(currencies_table['money_swis']) * 90
         # conversion_inr = float(currencies_table['money_inr']) * 1
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
      currencies_table = app_tables.currencies.get(user=self.user['username'])
      conversion_usd = float(currencies_table['money_usd'])*80
      conversion_euro = float(currencies_table['money_euro'])*85
      conversion_swis = float(currencies_table['money_swis']) * 90
      conversion_inr = float(currencies_table['money_inr']) * 1 
      if conversion_usd > 5000:
        currencies_table['money_usd'] = str((conversion_usd- 5000)/80)
        currencies_table.update()
      elif conversion_euro  > 5000:
        currencies_table['money_euro'] = str((conversion_euro- 5000)/85)
        currencies_table.update()
      elif conversion_swis > 5000:
        currencies_table['money_swis'] = str((conversion_swis - 5000) / 90)
        currencies_table.update()
      elif conversion_inr > 5000:
        currencies_table['money_inr'] = str((conversion_inr - 5000) / 1)
        currencies_table.update()
      else:
        self.label_4.text = "Insufficient funds"

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


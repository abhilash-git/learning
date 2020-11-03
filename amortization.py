# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rxhdZqvXZ87tK2CUHyWIa8Nq1FHCZE9z
"""

from datetime import datetime,date,timedelta
import calendar
def getMonthwithIndex(index=0,date_in=datetime.now()):
    days_in_month=0
    date_in = date_in.replace(day=1)
    for i in range(index):
      days_in_month = calendar.monthrange(date_in.year, date_in.month)[1]
      date_in = date_in + timedelta(days=days_in_month)
    return date_in

!pip install numpy-financial
import numpy_financial as npf
import pandas as pd
pd.options.display.float_format = '{:.5f}'.format

class Loan:
  def __init__(self, principle_amount, interest_in_year, period_in_years,starting_date=datetime.now()):
    self.starting_date = starting_date
    self.principle_amount = principle_amount
    self.interest_in_year = interest_in_year
    self.period_in_years = period_in_years
    self.column_names = ["MONTH", "STARTING_AMOUNT", "EMI_AMOUNT", "INTEREST_PAID", "PRINCIPLE_PAID", "LEFTOVER_PRINCIPLE"]
    self.df = pd.DataFrame(columns = self.column_names)
    self.emi_amount = npf.pmt((interest_in_year/100)/12, period_in_years*12, -principle_amount,0)
    self.Principle_paid=0
    self.Interest_paid=0

  def getPrincipleAmount(self):
      return self.principle_amount

  def setPrincipleAmount(self):
    self.principle_amount = self.principle_amount - self.Principle_paid

  def getDataFrame(self):
    return self.df

  def populateDateFrame(self):
    for i in range(0,self.period_in_years*12):
      temp_list_one_row=[]
      # print(i)
      temp_list_one_row.append(getMonthwithIndex(i).date())
      temp_list_one_row.append(self.getPrincipleAmount())
      temp_list_one_row.append(self.emi_amount)
      self.Interest_paid=(self.getPrincipleAmount()*(self.interest_in_year/100)/12)
      temp_list_one_row.append(self.Interest_paid)
      self.Principle_paid = self.emi_amount - self.Interest_paid
      temp_list_one_row.append(self.Principle_paid)
      temp_list_one_row.append(self.getPrincipleAmount() - self.Principle_paid)
      self.setPrincipleAmount()

      # print(temp_list_one_row)
      self.df = self.df.append(pd.Series(temp_list_one_row, index=self.column_names), ignore_index=True)

a=Loan(100000,13,30)

a.populateDateFrame()

a.getDataFrame()

import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
axes[0].plot(a.getDataFrame().MONTH,a.getDataFrame().STARTING_AMOUNT,color="blue")
axes[1].plot(a.getDataFrame().MONTH,a.getDataFrame().PRINCIPLE_PAID,color="red")
fig.tight_layout()

plt.show()


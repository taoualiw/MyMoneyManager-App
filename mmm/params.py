import os
from pathlib import Path
home = str(Path.home())
path_myfiles= home+ "/Documents/mmmData"
categMenuOption = (('Entertainment',
  'Dining Out',
  'Cinema/Theatre/Festival',
  'Museum',
  'Gaming',
  'To categorize'),
 ('General Expenses',
  'Groceries',
  'Clothing',
  'Amazon Shopping',
  'Home Maintenance',
  'Cash Withdrawal',
  'Gifts',
  'Categorize later',
  'To categorize'),
 ('Occasional Obligations',
  'Visa Fees',
  'Medical',
  'HD',
  'Transfert',
  'Tax',
  'To categorize'),
 ('Travel', 'Displacement', 'Hotel', 'Vacation', 'To categorize'),
 ('Immediate Obligations',
  'Internet',
  'Mobile',
  'Transportation',
  'Rent/Mortgage',
  'Electric',
  'Fitness',
  "Renter's/Home Insurance",
  'To categorize'),
 ('Refundable', 'Conference', 'Others', 'To categorize'),
 ('Income', 'To be Budgeted', 'To categorize'))

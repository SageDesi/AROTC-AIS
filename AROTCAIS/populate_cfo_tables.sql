use cfo;

INSERT INTO cfo_supercoa (SuperID, SuperID_Name)
VALUES (1, 'Asset');

INSERT INTO cfo_supercoa (SuperID, SuperID_Name)
VALUES (2, 'Liability');

INSERT INTO cfo_supercoa (SuperID, SuperID_Name)
VALUES (3, 'Equity');

INSERT INTO cfo_supercoa (SuperID, SuperID_Name)
VALUES (4, 'Revenue');

INSERT INTO cfo_supercoa (SuperID, SuperID_Name)
VALUES (5, 'Expense');

INSERT INTO cfo_coa (SubID, AccountCategory, AccountName, To_Increase, AccountDescription)
VALUES (1, 'Asset', 'GCASH', 'Debit', 'GCASH is an SMS-based application.');

import os

print("python3 20171404.py \"select max(A) from table1;\"")
os.system("python3 20171404.py \"select max(A) from table1;\"")

print("python3 20171404.py \"select min(B) from table2;\"")
os.system("python3 20171404.py \"select min(B) from table2;\"")

print("python3 20171404.py \"select avg(C) from table1;\"")
os.system("python3 20171404.py \"select avg(C) from table1;\"")

print("python3 20171404.py \"select sum(D) from table2;\"")
os.system("python3 20171404.py \"select sum(D) from table2;\"")

print("python3 20171404.py \"select A,D from table1,table2;\"")
os.system("python3 20171404.py \"select A,D from table1,table2;\"")

print("python3 20171404.py \"select distinct C from table1;\"")
os.system("python3 20171404.py \"select distinct C FROM table1;\"")

print("python3 20171404.py \"select B,C from table1 where A=-900;\"")
os.system("python3 20171404.py \"select B,C from table1 where A=-900;\"")

print("python3 20171404.py \"select A,B from table1 where A=775 OR B=803;\"")
os.system("python3 20171404.py \"select A,B from table1 where A=775 OR B=803;\"")

print("python3 20171404.py \"select * from table1,table2;\"")
os.system("python3 20171404.py \"select * from table1,table2;\"")

print("python3 20171404.py \"select * from table1,table2 where table1.B=table2.B;\"")
os.system("python3 20171404.py \"select * from table1,table2 where table1.B=table2.B;\"")

print("python3 20171404.py \"select A,D from table1,table2 where table1.B=table2.B;\"")
os.system("python3 20171404.py \"select A,D from table1,table2 where table1.B=table2.B;\"")

print("python3 20171404.py \"select table1.C from table1,table2 where table1.A<table2.B;\"")
os.system("python3 20171404.py \"select table1.C from table1,table2 where table1.A<table2.B;\"")

print("python3 20171404.py \"select A from table4;\"")
os.system("python3 20171404.py \"select A from table4;\"")

print("python3 20171404.py \"select Z from table1;\"")
os.system("python3 20171404.py \"select Z from table1;\"")

print("python3 20171404.py \"select B from table1,table2;\"")
os.system("python3 20171404.py \"select B from table1,table2;\"")

print("python3 20171404.py \"select distinct A,B from table1;\"")
os.system("python3 20171404.py \"select distinct A,B from table1;\"")

print("python3 20171404.py \"select table1.C from table1,table2 where table1.A<table2.D OR table1.A>table2.B;\"")
os.system("python3 20171404.py \"select table1.C from table1,table2 where table1.A<table2.D OR table1.A>table2.B;\"")

print("python3 20171404.py \"select table1.C from table1,table2 where table1.A=table2.D;\"")
os.system("python3 20171404.py \"select table1.C from table1,table2 where table1.A=table2.D;\"")

print("python3 20171404.py \"select table1.A from table1,table2 where table1.A<table2.B AND table1.A>table2.D;\"")
os.system("python3 20171404.py \"select table1.A from table1,table2 where table1.A<table2.B AND table1.A>table2.D;\"")

print("python3 20171404.py \"select sum(table1.A) from table1,table2;\"")
os.system("python3 20171404.py \"select sum(table1.A) from table1,table2;\"")

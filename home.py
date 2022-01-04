# -*- coding: utf-8 -*-
"""HOME.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/182C0Kcpn2C8v-8V79dS3cX5MMt__Dpai
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('hmeq.csv')

#Nhìn khái quát những dòng đầu tiên của tập dữ liệu
print('Số cột của tập dữ liệu:', df.shape[1])
print('Số dòng của tập dữ liệu:',df.shape[0])
df.head(10)

df.describe()

plt.figure(figsize=(16, 8))
fig, ax = plt.subplots()
df['LOAN'].plot.kde(ax=ax,legend=False,title='Số tiền')
df['LOAN'].hist(ax=ax,grid=False,density=True)
plt.xlabel('Số tiền',fontsize=16)
#plt.ylabel('Frequency')
plt.title('Số tiền KH muốn vay')
plt.show()

#Dữ liệu ở đây phân phối không đều và bị lệch về phía bên trái. Số tiền mà các KH muốn vay
#chiếm phần lớn từ 10000 - 30000$ và cao nhất ở khoảng 18000$

plt.figure(figsize=(16, 8))
fig, ax = plt.subplots()
df['MORTDUE'].plot.kde(ax=ax,legend=False,title='Số tiền thế chấp')
df['MORTDUE'].hist(ax=ax,grid=False,density=True)
plt.xlabel('Số tiền thế chấp',fontsize=16)
#plt.ylabel('Frequency')
plt.title('Số tiền KH thế chấp')
plt.show()

#Ta có thể thấy dữ liệu phân bố không đồng đều và bị lệch nhiều về phía bên trái. 
#Bên cạnh đó, ở biểu đồ histogram ta thấy có giá trị từ 35000 – 40000 xuất hiện riêng lẻ 
#nên rất có khả năng những giá trị này là những outlier của tập dữ liệu

plt.figure(figsize=(16, 8))
fig, ax = plt.subplots()
df['DEBTINC'].plot.kde(ax=ax,legend=False,title='Tỉ lệ')
df['DEBTINC'].hist(ax=ax,grid=False,density=True)
plt.xlabel('Tỉ lệ',fontsize=16)
#plt.ylabel('Frequency')
plt.title('Tỉ lệ nợ trên thu nhập')
plt.show()

plt.figure(figsize=(16, 8))
fig, ax = plt.subplots()
df["YOJ"].plot.kde(ax=ax,legend=False,title='Số năm làm việc')
df["YOJ"].hist(ax=ax,grid=False,density=True)
plt.xlabel('Số năm làm việc',fontsize=16)
#plt.ylabel('Frequency')
plt.title('Số năm làm việc')
plt.show()

#Số lượng hồ sơ cho vay nhà ở nhóm người có có số năm làm việc chưa tới 1 năm chiếm tỷ lệ cao nhất với hơn 800 bộ hồ sơ
#Số lượng năm làm việc càng lớn thì số lượng hồ sơ cho vay nhà lại càng giảm

plt.figure(figsize=(16, 8))
fig, ax = plt.subplots()
df["VALUE"].plot.kde(ax=ax,legend=False,title='Số năm làm việc')
df["VALUE"].hist(ax=ax,grid=False,density=True)
plt.xlabel('Số năm làm việc',fontsize=16)
#plt.ylabel('Frequency')
plt.title('Số năm làm việc')
plt.show()

"""**Xử lý null**"""

nan_many = df[df['MORTDUE'].isna() & df['VALUE'].isna() & df['REASON'].isna() & df['JOB'].isna()]
print(nan_many.shape)
nan_many
#Show ra những điểm dữ liệu missing ở phần lớn các cột
# Ta thấy có 9 dòng có phần lớn dữ liệu ở các cột là NULL, nên ta sẽ DROP 9 dòng này

#Xóa bỏ các điểm dữ liệu trên
df.drop(index=nan_many.index, inplace = True)
df = df.reset_index(drop=True)
df[df['MORTDUE'].isna() & df['VALUE'].isna() & df['REASON'].isna() & df['JOB'].isna()]

"""**Fill NULL**"""

df=df.replace(np.nan, 0)# thay thế các null bằng giá trị 0

"""**Xem biểu đồ**"""

hist_figsize = (15, 2)
binwidth = 5

f, ax = plt.subplots(1, 3, sharey=True, figsize=hist_figsize)
sns.boxplot(data=df, ax=ax[0], x='LOAN')
sns.boxplot(data=df, ax=ax[1], x='MORTDUE')
sns.boxplot(data=df, ax=ax[2], x='VALUE')
f.tight_layout()

f, ax = plt.subplots(1, 2, sharey=True, figsize=hist_figsize)
sns.boxplot(data=df, ax=ax[0], x='DEROG')
sns.boxplot(data=df, ax=ax[1], x='DELINQ')
f.tight_layout()

f, ax = plt.subplots(1, 2, sharey=True, figsize=hist_figsize)
sns.boxplot(data=df, ax=ax[0], x='NINQ')
sns.boxplot(data=df, ax=ax[1], x='CLNO')
f.tight_layout()

f, ax = plt.subplots(figsize=hist_figsize)
sns.boxplot(data=df, ax=ax, x='DEBTINC')
f.tight_layout()
# Có Outlier xuất hiện khá nhiều ở cột DEBTIN

"""# **Xác định outliners bằng IQR**

IQR là sự khác biệt giữa tứ phân vị thứ nhất Q1 và tứ phân vị thứ ba Q3:

IQR=Q3−Q1

Giá trị IQR có thể sử dụng để xác định outliers bằng cách thiết lập các giá trị biên Upper/Lower giống với phương pháp STD như sau: Nếu chúng ta trừ đi kxIQR từ tứ phân vị đầu tiên Q1, bất kỳ giá trị dữ liệu nào nhỏ hơn con số này được coi là giá trị outliers. Tương tự như vậy, nếu chúng ta thêm kxIQR đến tứ phân vị thứ ba Q3, bất kỳ giá trị dữ liệu nào lớn hơn con số này được coi là outliers. Giá trị k thường được chọn là 1.5. Trong trường hợp xác định các extreme outliers có thể dùng giá trị k = 3.

Các bước xác định outliers bằng phương pháp IQR:


*   Bước 1: Tính IQR
*   Bước 2: Tính giá trị biên Upper/Lower để xác định outliers
*   Bước 3: Xác định và loại bỏ outliers dựa trên giá trị biên





"""

#Tính IQR
q25, q75 = np.percentile(df["LOAN"], 25), np.percentile(df["LOAN"], 75)
iqr = q75 - q25
# Tính giá trị biên Upper/Lower để xác định outliers
limit_iqr = 1.5*iqr
lower_iqr, upper_iqr = q25 - limit_iqr, q75 + limit_iqr
#remove outliers
df.drop(df[df['LOAN'] < lower_iqr].index,inplace = True)
df.drop(df[df['LOAN'] > upper_iqr].index,inplace = True)

#Tính IQR
q25, q75 = np.percentile(df["MORTDUE"], 25), np.percentile(df["MORTDUE"], 75)
iqr = q75 - q25
# Tính giá trị biên Upper/Lower để xác định outliers
limit_iqr = 1.5*iqr
lower_iqr, upper_iqr = q25 - limit_iqr, q75 + limit_iqr
#remove outliers
df.drop(df[df['MORTDUE'] < lower_iqr].index,inplace = True)
df.drop(df[df['MORTDUE'] > upper_iqr].index,inplace = True)

#Tính IQR
q25, q75 = np.percentile(df["VALUE"], 25), np.percentile(df["VALUE"], 75)
iqr = q75 - q25
# Tính giá trị biên Upper/Lower để xác định outliers
limit_iqr = 1.5*iqr
lower_iqr, upper_iqr = q25 - limit_iqr, q75 + limit_iqr
#remove outliers
df.drop(df[df['VALUE'] < lower_iqr].index,inplace = True)
df.drop(df[df['VALUE'] > upper_iqr].index,inplace = True)

#Tính IQR
q25, q75 = np.percentile(df["DEROG"], 25), np.percentile(df["DEROG"], 75)
iqr = q75 - q25
# Tính giá trị biên Upper/Lower để xác định outliers
limit_iqr = 1.5*iqr
lower_iqr, upper_iqr = q25 - limit_iqr, q75 + limit_iqr
#remove outliers
df.drop(df[df['DEROG'] < lower_iqr].index,inplace = True)
df.drop(df[df['DEROG'] > upper_iqr].index,inplace = True)

#Tính IQR
q25, q75 = np.percentile(df["DELINQ"], 25), np.percentile(df["DELINQ"], 75)
iqr = q75 - q25
# Tính giá trị biên Upper/Lower để xác định outliers
limit_iqr = 1.5*iqr
lower_iqr, upper_iqr = q25 - limit_iqr, q75 + limit_iqr
#remove outliers
df.drop(df[df['DELINQ'] < lower_iqr].index,inplace = True)
df.drop(df[df['DELINQ'] > upper_iqr].index,inplace = True)

#Tính IQR
q25, q75 = np.percentile(df["NINQ"], 25), np.percentile(df["NINQ"], 75)
iqr = q75 - q25
# Tính giá trị biên Upper/Lower để xác định outliers
limit_iqr = 1.5*iqr
lower_iqr, upper_iqr = q25 - limit_iqr, q75 + limit_iqr
#remove outliers
df.drop(df[df['NINQ'] < lower_iqr].index,inplace = True)
df.drop(df[df['NINQ'] > upper_iqr].index,inplace = True)

#Tính IQR
q25, q75 = np.percentile(df["CLNO"], 25), np.percentile(df["CLNO"], 75)
iqr = q75 - q25
# Tính giá trị biên Upper/Lower để xác định outliers
limit_iqr = 1.5*iqr
lower_iqr, upper_iqr = q25 - limit_iqr, q75 + limit_iqr
#remove outliers
df.drop(df[df['CLNO'] < lower_iqr].index,inplace = True)
df.drop(df[df['CLNO'] > upper_iqr].index,inplace = True)

#Tính IQR
q25, q75 = np.percentile(df["DEBTINC"], 25), np.percentile(df["DEBTINC"], 75)
iqr = q75 - q25
# Tính giá trị biên Upper/Lower để xác định outliers
limit_iqr = 1.5*iqr
lower_iqr, upper_iqr = q25 - limit_iqr, q75 + limit_iqr
#remove outliers
df.drop(df[df['DEBTINC'] < lower_iqr].index,inplace = True)
df.drop(df[df['DEBTINC'] > upper_iqr].index,inplace = True)

"""**Nhận xét: Quan sát biểu đồ ta có thể thấy hầu hết các outliners đã được loại bỏ**"""

hist_figsize = (15, 2)
binwidth = 5

f, ax = plt.subplots(1, 3, sharey=True, figsize=hist_figsize)
sns.boxplot(data=df, ax=ax[0], x='LOAN')
sns.boxplot(data=df, ax=ax[1], x='MORTDUE')
sns.boxplot(data=df, ax=ax[2], x='VALUE')
f.tight_layout()

f, ax = plt.subplots(1, 2, sharey=True, figsize=hist_figsize)
sns.boxplot(data=df, ax=ax[0], x='DEROG')
sns.boxplot(data=df, ax=ax[1], x='DELINQ')
f.tight_layout()

f, ax = plt.subplots(1, 2, sharey=True, figsize=hist_figsize)
sns.boxplot(data=df, ax=ax[0], x='NINQ')
sns.boxplot(data=df, ax=ax[1], x='CLNO')
f.tight_layout()

f, ax = plt.subplots(figsize=hist_figsize)
sns.boxplot(data=df, ax=ax, x='DEBTINC')
f.tight_layout()
# Có Outlier xuất hiện khá nhiều ở cột DEBTIN
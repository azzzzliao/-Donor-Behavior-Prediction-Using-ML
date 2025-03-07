#!/usr/bin/env python 
# -*- coding: utf8 -*-  
# Note the first line in the above is for Operating system, the  
# second line is for Python interpreter 

from datetime import datetime
import pandas as pd
import numpy as np
import csv


#1. Load Data
df = pd.read_csv('ABC.csv')
#2. Delete unneccessary columns
df = df.drop(columns=['periodic_total_amount', 'payment_id', 'last_status', 'periodic_status', 'periodic_success_times', 'payment_time', 'tax_credit', 'donation_name'])

#3. Add new column:donater_type
def map_donation_type(description):
    if '定期' in description:
        return '1'
    else:
        return '0'

df['donater_type'] = df['payment_type'].apply(lambda x: map_donation_type(x))

df.drop(columns=['payment_type'], inplace=True)

df.rename(columns={'payment_type': 'donater_type'}, inplace=True)

#4. Add new column:gender
df['uid'] = df['uid'].astype(str)

def map_uid(uid):
    if len(uid) == 10:
        if uid[1] == '1':
            return '1'
        elif uid[1] == '2':
            return '0'
    elif len(uid) == 8:
        return '2'
    else:
        return '-1'
df['category'] = df['uid'].apply(lambda x: map_uid(x))

df = df.drop(columns=['uid'])

#5. Add new column:city
df['address'] = df['address'].astype(str)

def city_donation_type(description):
    if '新北市' in description:
        return '31'
    elif '新竹市' in description:
        return '12'
    elif '新竹縣' in description:
        return '33'
    elif '基隆' in description:
        return '11'
    elif '桃園市' in description:
        return '32'
    elif '苗栗' in description:
        return '35'
    elif '台中' in description or '臺中' in description:
        return '03'
    elif '彰化' in description:
        return '37'
    elif '雲林' in description:
        return '39'
    elif '南投' in description:
        return '38'
    elif '嘉義縣' in description:
        return '40'
    elif '嘉義市' in description:
        return '22'
    elif '台南' in description or '臺南' in description:
        return '05'
    elif '高雄' in description:
        return '07'
    elif '屏東' in description:
        return '43'
    elif '宜蘭' in description:
        return '34'
    elif '花蓮' in description:
        return '45'
    elif '台東' in description or '臺東' in description:
        return '46'
    elif '澎湖' in description:
        return '44'
    elif '金門' in description:
        return '90'
    elif '連江' in description:
        return '91'
    elif '北市' in description:
        return '01'
    else:
        return '-1'

df['city'] = df['address'].apply(lambda x: city_donation_type(x))

df.drop(columns=['address'], inplace=True)

#6 Replace date by month
df['date']= pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df.drop(columns=['date'], inplace=True)

#7 tax
def tax_donation_type(description):
    if '國稅局' in description or '需寄' in description:
        return '1'
    else:
        return '0'
df['tax'] = df['receipt_type'].apply(lambda x : tax_donation_type(x))

df.drop(columns=['receipt_type'], inplace=True)

#8. Reorder the dataframe from donation_id > date

donation_group = df.groupby(['donation_id'])
df = df.sort_values(by = ['year', 'donation_id', 'month'])
df.info()

#9. Reorder the columns
new_order = ['donation_id', 'donater_type', 'category', 'year', 'month', 'amount', 'city', 'tax', 'name']
df = df.reindex(columns=new_order)

#10. breakpoint_finish_cleaning write to dataframe
pd.DataFrame.to_csv(df, 'test.csv', index = None)

#11. amount group by category
category_group = df.groupby(['category'])

category_list = []
for (key,), group in category_group:
    dict_category = dict()
    dict_category['category'] = key
    dict_category['total_amount'] = group['amount'].sum()
    category_list.append(dict_category)
with open('category_amount.csv', 'w', newline='') as csvfile:
    fieldnames = ['category', 'total_amount']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for i in range(len(category_list)):
        writer.writerow(category_list[i])

#12. amount group by city
city_group = df.groupby(['city'])

city_list = []
for (key,), group in city_group:
    dict_city = dict()
    dict_city['city'] = key
    dict_city['total_amount'] = group['amount'].sum()
    city_list.append(dict_city)
with open('city_amount.csv', 'w', newline='') as csvfile:
    fieldnames = ['city', 'total_amount']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for i in range(len(city_list)):
        writer.writerow(city_list[i])

#13. amount group by months
monthly_group = df.groupby(df['month'])

monthly_list = []
for key, group in monthly_group:
    dict_monthly = dict()
    dict_monthly['monthly'] = key
    dict_monthly['total_amount'] = group['amount'].sum()
    monthly_list.append(dict_monthly)
with open('monthly_amount.csv', 'w', newline='') as csvfile:
    fieldnames = ['monthly', 'total_amount']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for i in range(len(monthly_list)):
        writer.writerow(monthly_list[i])

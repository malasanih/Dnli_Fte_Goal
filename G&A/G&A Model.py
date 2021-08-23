#!/usr/bin/env python
# coding: utf-8

# In[174]:


import pandas as pd
import numpy as np
import openpyxl
import itertools
import datetime


# In[175]:


drivers = pd.read_csv('G&A Drivers.csv')
summary = pd.read_csv('G&A Summary.csv')
pd.set_option("display.max_columns", 50)
pd.set_option('display.max_rows', None)


# In[171]:


#drivers['start'] = pd.to_datetime(drivers['start'])
#drivers['end'] = pd.to_datetime(drivers['end'])
#drivers.head()


# In[176]:


def output_maker(drivers):
    
    #Creates output DataFrame structure from DataFrame that is in the same format as 'LRP Data.csv' - date columns must be in pd.DateTime format
    #Creates one row per month per study
    
    data = pd.DataFrame(columns = ['Month', 'Year', 'HC All', 'HC Office', 'HC Lab', 'HC Manufacturing', 'Collaborations', 'Growth Rate', 'Growth', 'Locations High FTE', 'Locations Low FTE', 'Commercial', 'Planned Collaborations', 'Combined Programs', 'International Expansion', 'China Expansion', 'Phase 3 Trial', 'Commercial Partnered Program'])
    for i in range(len(drivers)):
        hc_all = drivers.denali_hc_all[i]
        hc_office = drivers.denali_hc_office[i]
        hc_lab = drivers.denali_hc_lab[i]
        hc_manufacturing = drivers.denali_manufacturing_hc[i]
        collaborations = drivers.collaborations[i]
        growth_rate = drivers.growth_rate[i]
        growth = drivers.growth[i]
        locations_high_fte = drivers.locations_high_fte[i]
        locations_low_fte = drivers.locations_low_fte[i]
        commercial = drivers.commercial[i]
        planned_collabs = drivers.planned_collabs[i]
        combined_programs = drivers.combined_programs[i]
        international_expansion = drivers.international_expansion[i]
        china_expansion = drivers.china_expansion[i]
        ph3_trial = drivers.ph3_trial[i]
        comm_partnered_program = drivers.partnered_program[i]
        start_month = drivers.start[i].month
        start_year = drivers.start[i].year
        end_month = drivers.end[i].month
        end_year = drivers.end[i].year


        #Optional case (not currently used) if only study_start and csr dates are available. Change starting condition to use 
        for year in range(start_year, end_year + 1):
            for month in range(1, 12+1):
                if year == start_year and month < start_month:
                    continue
                if year == end_year and month > end_month:
                    break
                if year == end_year and month == end_month:
                    data = data.append(pd.DataFrame([[month, year, hc_all, hc_office, hc_lab, hc_manufacturing, collaborations, growth_rate, growth, locations_high_fte, locations_low_fte, commercial, planned_collabs, combined_programs, international_expansion, china_expansion, ph3_trial, comm_partnered_program]], columns = ['Month', 'Year', 'HC All', 'HC Lab', 'HC Office', 'HC Manufacturing', 'Collaborations', 'Growth Rate', 'Growth', 'Locations High FTE', 'Locations Low FTE', 'Commercial', 'Planned Collaborations', 'Combined Programs', 'International Expansion', 'China Expansion', 'Phase 3 Trial', 'Commercial Partnered Program']))
                else:
                    data = data.append(pd.DataFrame([[month, year, hc_all, hc_office, hc_lab, hc_manufacturing, collaborations, growth_rate, growth, locations_high_fte, locations_low_fte, commercial, planned_collabs, combined_programs, international_expansion, china_expansion, ph3_trial, comm_partnered_program]], columns = ['Month', 'Year', 'HC All', 'HC Lab', 'HC Office', 'HC Manufacturing', 'Collaborations', 'Growth Rate', 'Growth', 'Locations High FTE', 'Locations Low FTE', 'Commercial', 'Planned Collaborations', 'Combined Programs', 'International Expansion', 'China Expansion', 'Phase 3 Trial', 'Commercial Partnered Program']))
       


    # Returns a DataFrame with one row per month per study
    data = data.reset_index().drop('index', axis=1)
    return data

def fte_calculator(row):
    if row['Fixed or Variable'] == 'Fixed':
        row['Demand'] = row['Fixed Demand']
    
    if row['Business Unit'] == 'Business Operations':
        if row['Role'] == 'IP':
            row['Demand'] = row['Baseline Variable Demand'] * row['Combined Programs']
        if row['Role'] == 'Contracting':
            row['Demand'] = row['HC All'] * row['Baseline Variable Demand']
        if row['Role'] == 'General Counsel':
            row['Demand'] = row['HC All'] * row['Baseline Variable Demand']
        if row['Role'] == 'Legal Operations':
            row['Demand'] = row['HC All'] * row['Baseline Variable Demand']
        if row['Role'] == 'Business Development':
            row['Demand'] = row['Baseline Variable Demand'] * row['Planned Collaborations']
        if row['Role'] == 'Alliance Mgmt Collaborations':
            row['Demand'] = row['Baseline Variable Demand'] * row['Collaborations']
        if row['Role'] == 'Alliance Mgmt China':
            row['Demand'] = row['Baseline Variable Demand'] * row['China Expansion']
        if row['Role'] == 'Alliance Mgmt Commercial':
            row['Demand'] = row['Baseline Variable Demand'] * row['Commercial Partnered Programs']
    if row['Business Unit'] == 'Finance':
        if row['Role'] == 'IT Support':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC All']
        if row['Role'] == 'Controller - Commercial':
            row['Demand'] = row['Baseline Variable Demand'] * row['Commercial']
        if row['Role'] == 'Controller - International':
            row['Demand'] = row['Baseline Variable Demand'] * row['International Expansion']
        if row['Role'] == 'Controller - China':
            row['Demand'] = row['Baseline Variable Demand'] * row['China Expansion']
        if row['Role'] == 'Controller - Collaborations':
            row['Demand'] = row['Baseline Variable Demand'] * row['Planned Collaborations']
        if row['Role'] == 'Controller':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC All']
        if row['Role'] == 'Tax - SALT':
            row['Demand'] = row['Baseline Variable Demand'] * row['Commercial']
        if row['Role'] == 'Tax - International':
            row['Demand'] = row['Baseline Variable Demand'] * row['Commercial']
        if row['Role'] == 'Procurement':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC All']
        if row['Role'] == 'Procurement - New Locations':
            row['Demand'] = 0 #accounted for in overall procurement role
        if row['Role'] == 'Procurement - Ph 3 Trial':
            row['Demand'] = row['Baseline Variable Demand'] * row['Phase 3 Trial']
        if row['Role'] == 'Investor Relations':
            row['Demand'] = row['Baseline Variable Demand'] * row['Commercial']
        if row['Role'] == 'Communications':
            row['Demand'] = row['Baseline Variable Demand'] * row['Commercial']
        if row['Role'] == 'Facilities - Office':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC Office']
        if row['Role'] == 'Facilities - Lab':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC Lab']
        if row['Role'] == 'R&D Finance':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC All']
    if row['Business Unit'] == 'HR':
        if row['Role'] == 'HR Payroll':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC All']
        if row['Role'] == 'HR Operations':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC All']
        if row['Role'] == 'HR Business Partners':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC All']
        if row['Role'] == 'Talent Acquisition':
            row['Demand'] = row['Baseline Variable Demand'] * row['Growth']
        if row['Role'] == 'Administration':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC All']
        if row['Role'] == 'Compliance & Employee Relations':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC Manufacturing']
        if row['Role'] == 'Organizational Design & Training - Manufacturing':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC Manufacturing']
        if row['Role'] == 'Organizational Design & Training - Commercial':
            row['Demand'] = row['Baseline Variable Demand'] * row['Commercial']
        if row['Role'] == 'EH&S - Office':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC Office']
        if row['Role'] == 'EH&S - Lab':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC Lab']
        if row['Role'] == 'EH&S - Manufacturing':
            row['Demand'] = row['Baseline Variable Demand'] * row['HC Manufacturing']

def ga_fte(drivers):
    output_timeline = drivers
    resourcing_summary = pd.read_csv('G&A Summary.csv')
    #resourcing_summary = resourcing_summary[resourcing_summary['Role'] == 'Facilities - Lab']
    
    #Create output data structure with one row per role per month per study
    df = output_timeline.assign(key=1).merge(resourcing_summary.assign(key=1), how='outer', on='key')

    #Add additional columns to output table
    df['Demand'] = 0

    #Iterate through each row of output table and fill in the Pre-SEED Demand and Demand column
    rows = []
    for index,row in df.iterrows():
        d = row.to_dict()
        fte_calculator(d)
        rows.append(d)
    output = pd.DataFrame(rows)
    
    return output[['Role', 'Business Unit', 'Home Department', 'Cost Number', 'Fixed or Variable', 'Year', 'Demand']]
            
            
            


# In[177]:


ga_fte(drivers).to_excel('G&A OUTPUT.xlsx')


# In[ ]:





# In[ ]:





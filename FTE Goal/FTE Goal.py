#!/usr/bin/env python
# coding: utf-8

# In[423]:


import pandas as pd
import numpy as np
import openpyxl
import itertools
import datetime


# In[424]:


#Loads in resourcing summary file as a DataFrame
resourcing_summary = pd.read_csv('Resourcing Summary Assumptions.csv')

pd.set_option("display.max_columns", 50)
pd.set_option('display.max_rows', None)


# In[425]:


#Loads in LRP Data as a DataFrame
lrp = pd.read_csv('Model Resourcing Assumptions_2021Aug23.csv')
lrp


# In[415]:


#Copies LRP DataFrame with date columns in pd.Datetime format

lrp_data = pd.DataFrame()
lrp_data['clin_study_number'] = lrp['clin_study_number']
lrp_data['program'] = lrp['program']
lrp_data['trial_stage'] = lrp['trial_stage']
lrp_data['no_of_subjects'] = lrp['no_of_subjects']
lrp_data['no_of_countries'] = lrp['no_of_countries']
lrp_data['no_of_denali_employees'] = lrp['no_of_denali_employees']
lrp_data['no_of_sites'] = lrp['no_of_sites']
lrp_data['study_start'] = pd.to_datetime(lrp['study_start'])
lrp_data['fpi'] = pd.to_datetime(lrp['fpi'])
lrp_data['lpi'] = pd.to_datetime(lrp['lpi'])
lrp_data['lpo'] = pd.to_datetime(lrp['lpo'])
lrp_data['dbl'] = pd.to_datetime(lrp['dbl'])
lrp_data['top_line_results'] = pd.to_datetime(lrp['top_line_results'])
lrp_data['csr'] = pd.to_datetime(lrp['csr'])
lrp_data['clinical_vendors'] = lrp['clinical_vendors']
lrp_data['biometric_vendors'] = lrp['biometric_vendors']
lrp_data['study_or_ole'] = lrp['study_or_ole']
lrp_data['registrational_potential'] = lrp['registrational_potential']
lrp_data['kol_demand'] = lrp['kol_demand']
lrp_data['small_or_large'] = lrp['small_or_large']
lrp_data['trial_complexity'] = lrp['trial_complexity']
lrp_data['core_or_seed'] = lrp['Core or SEED Program']
lrp_data['pts'] = lrp['PTS']
lrp_data = lrp_data.iloc[0:146]
lrp_data


# In[416]:


#Algorithm helper functions defined first

def output_timeline_maker(lrp_data):
    
    #Creates output DataFrame structure from DataFrame that is in the same format as 'LRP Data.csv' - date columns must be in pd.DateTime format
    #Creates one row per month per study
    
    data = pd.DataFrame(columns = ['Study Number', 'Program', 'Trial Stage', 'Subjects', 'Countries', 'Employees', 'Sites', 'Clinical Vendors', 'Biometric Vendors', 'Study or OLE', 'Reg Pot', 'KOL Demand', 'Small or Large Molecule', 'Trial Complexity', 'Core or SEED','Month', 'Year', 'Previous Milestone'])
    for i in range(len(lrp_data)):
        #If any additional columns are added to the input file (ex: number of markets, device Y/N, etc.) reflect those changes within this function.
        clin_study_number = lrp_data.clin_study_number[i]
        program = lrp_data.program[i]
        trial_stage = lrp_data.trial_stage[i]
        no_of_subjects = lrp_data.no_of_subjects[i]
        no_of_countries = lrp_data.no_of_countries[i]
        no_of_denali_employees = lrp_data.no_of_denali_employees[i]
        no_of_sites = lrp_data.no_of_sites[i]
        clinical_vendors = lrp_data.clinical_vendors[i]
        biometric_vendors = lrp_data.biometric_vendors[i]
        study_or_ole = lrp_data.study_or_ole[i]
        registrational_potential = lrp_data.registrational_potential[i]
        kol_demand = lrp_data.kol_demand[i]
        small_or_large = lrp_data.small_or_large[i]
        core_or_seed = lrp_data.core_or_seed[i]
        pts = lrp_data.pts[i]
        trial_complexity = lrp_data.trial_complexity[i]
        
        start_month = int(lrp_data.study_start[i].month)
        start_year = int(lrp_data.study_start[i].year)
        fpi_month = lrp_data.fpi[i].month 
        fpi_year = lrp_data.fpi[i].year
        end_month = lrp_data.csr[i].month
        end_year = lrp_data.csr[i].year
        
        
        #Creates ramp-up rows, with 4 month ramp-up for phase 0 trials, 6 month ramp-up for phase 1, 1b, 2, or 1/2 trials, and 9 month ramp-up for phase 2/3 and 3 trials
        ramp_up_length = 4
        if lrp_data.trial_stage[i] == '1' or lrp_data.trial_stage[i] == '1b' or lrp_data.trial_stage[i] == '2' or lrp_data.trial_stage[i] == '1/2':
            ramp_up_length = 6
        elif lrp_data.trial_stage[i] == '2/3' or lrp_data.trial_stage[i] == '3':
            ramp_up_length = 9
        if lrp_data.study_or_ole[i] == 'OLE':
            ramp_up_length = 2
        if lrp_data.trial_stage[i] == 'Filing' or lrp_data.trial_stage[i] == 'All':
            ramp_up_length = 0
            
        
        ramp_up_month = fpi_month - ramp_up_length
        ramp_up_year = fpi_year
        if ramp_up_month <= 0:
            ramp_up_month = fpi_month + (12 - ramp_up_length)
            ramp_up_year = fpi_year - 1     
        
        if (ramp_up_month < start_month and ramp_up_year == start_year) or (ramp_up_year < start_year):
            ramp_up_time = start_month - ramp_up_month
            if ramp_up_time <= 0:
                ramp_up_time = (12 + start_month) - ramp_up_month
            for _ in range(ramp_up_time):
                data = data.append(pd.DataFrame([[clin_study_number, program, trial_stage, no_of_subjects, no_of_countries, no_of_denali_employees, no_of_sites, clinical_vendors, biometric_vendors, study_or_ole, registrational_potential, kol_demand, small_or_large, trial_complexity, core_or_seed, pts, ramp_up_month, ramp_up_year, 'ramp_up']], columns = ['Study Number', 'Program', 'Trial Stage', 'Subjects', 'Countries', 'Employees', 'Sites', 'Clinical Vendors', 'Biometric Vendors', 'Study or OLE', 'Reg Pot', 'KOL Demand', 'Small or Large Molecule', 'Trial Complexity', 'Core or SEED', 'PTS', 'Month', 'Year', 'Previous Milestone']))
                ramp_up_month += 1
                if ramp_up_month > 12:
                    ramp_up_month = 1
                    ramp_up_year += 1

        #Optional case (not currently used) if only study_start and csr dates are available. Change starting condition to use 
        if lrp_data.trial_stage[i] == '5':
            for year in range(start_year, end_year + 1):
                for month in range(1, 12+1):
                    if year == start_year and month < start_month:
                        continue
                    if year == end_year and month > end_month:
                        break
                    if year == end_year and month == end_month:
                        data = data.append(pd.DataFrame([[clin_study_number, program, trial_stage, no_of_subjects, no_of_countries, no_of_denali_employees, no_of_sites, clinical_vendors, biometric_vendors, study_or_ole, registrational_potential, kol_demand, small_or_large, trial_complexity, core_or_seed, pts, month, year, 'csr']], columns = ['Study Number', 'Program', 'Trial Stage', 'Subjects', 'Countries', 'Employees', 'Sites', 'Clinical Vendors', 'Biometric Vendors', 'Study or OLE', 'Reg Pot', 'KOL Demand', 'Small or Large Molecule', 'Trial Complexity', 'Core or SEED', 'PTS', 'Month', 'Year', 'Previous Milestone']))
                    else:
                        data = data.append(pd.DataFrame([[clin_study_number, program, trial_stage, no_of_subjects, no_of_countries, no_of_denali_employees, no_of_sites, clinical_vendors, biometric_vendors, study_or_ole, registrational_potential, kol_demand, small_or_large, trial_complexity, core_or_seed, pts, month, year, 'fpi']], columns = ['Study Number', 'Program', 'Trial Stage', 'Subjects', 'Countries', 'Employees', 'Sites', 'Clinical Vendors', 'Biometric Vendors', 'Study or OLE', 'Reg Pot', 'KOL Demand', 'Small or Large Molecule', 'Trial Complexity', 'Core or SEED', 'PTS', 'Month', 'Year', 'Previous Milestone']))
       
        #Creates one output DataFrame, with previous_milestone column containing the most recent milestone hit for a given month 
        else:
            fpi = (lrp_data.fpi[i].month, lrp_data.fpi[i].year)
            lpi = (lrp_data.lpi[i].month, lrp_data.lpi[i].year)
            lpo = (lrp_data.lpo[i].month, lrp_data.lpo[i].year)
            dbl = (lrp_data.dbl[i].month, lrp_data.dbl[i].year)
            tlr = (lrp_data.top_line_results[i].month, lrp_data.top_line_results[i].year)
            csr = (lrp_data.csr[i].month, lrp_data.csr[i].year)

            milestone_dict = {fpi: 'fpi', lpi: 'lpi', lpo: 'lpo', dbl: 'dbl', tlr: 'top_line_results', csr: 'csr'}

            milestone = 'study_start'
            for year in range(start_year, end_year + 1):
                for month in range(1, 12+1):
                    if (month, year) in milestone_dict:
                        milestone = milestone_dict[(month, year)]
                    if year == start_year and month < start_month:
                        continue
                    if year == end_year and month > end_month:
                        break

                    data = data.append(pd.DataFrame([[clin_study_number, program, trial_stage, no_of_subjects, no_of_countries, no_of_denali_employees, no_of_sites, clinical_vendors, biometric_vendors, study_or_ole, registrational_potential, kol_demand, small_or_large, trial_complexity, core_or_seed, pts, month, year, milestone]], columns = ['Study Number', 'Program', 'Trial Stage', 'Subjects', 'Countries', 'Employees', 'Sites', 'Clinical Vendors', 'Biometric Vendors', 'Study or OLE', 'Reg Pot', 'KOL Demand', 'Small or Large Molecule', 'Trial Complexity', 'Core or SEED', 'PTS', 'Month', 'Year', 'Previous Milestone']))

    # Returns a DataFrame with one row per month per study
    data = data.reset_index().drop('index', axis=1)
    return data

def ongoing_studies_finder(output_df, month, year):
    
    #Finds the number of ongoing_studies
    all_studies = output_df
    month_filter = all_studies[all_studies['Month'] == month]
    month_year_filter = month_filter[month_filter['Year'] == year]
    return len(month_year_filter.groupby('Study Number').count())

def ongoing_molecules_finder(output_df, month, year):
    
    #Finds the number of ongoing programs
    all_studies = output_df
    month_filter = all_studies[all_studies['Month'] == month]
    month_year_filter = month_filter[month_filter['Year'] == year]
    return len(month_year_filter.groupby('Program').count())

def study_efficiency_finder(output_df, trial_stage, program, month, year):
    
    #Finds whether or not to apply efficiency -- True if there are more than one ongoing studies in a given phase for a given program, False otherwise
    all_studies = output_df
    month_filter = all_studies[all_studies['Month'] == month]
    year_filter = month_filter[month_filter['Year'] == year]
    trial_stage_filter = year_filter[year_filter['Trial Stage'] == trial_stage ]
    program_filter = trial_stage_filter[trial_stage_filter['Program'] == program]
    return len(program_filter.groupby('Study Number').count()) > 1

def ongoing_core_studies(output_df, month, year):
    
    #Finds number of ongoing Core studies
    core_studies = output_df[output_df['Core or SEED'] == 'Core']
    month_filter = core_studies[core_studies['Month'] == month]
    year_filter = month_filter[month_filter['Year'] == year]
    return len(year_filter.groupby('Study Number').count())
    
        
def fte_calculator(row, df, partner, employees):
    
    #Calculates FTE demand -- fills in 'Demand' column of the output table, one row at a time. References values in other columns of that row to do so.
    #If Role is fixed, allocate an equivalent fraction of fixed demand to Core studies only based on the number of ongoing core studies

    if row['Fixed or Variable'] == 'Fixed':
        ongoing_core = ongoing_core_studies(df, row['Month'], row['Year'])
        if row['Core or SEED'] == 'Core':
            row['All-in Demand'] = row['Fixed Demand'] / ongoing_core
            row['PTS Demand'] = row['Fixed Demand'] / ongoing_core
    
    #If role is variable, calculate demand based on appropriate drivers and multipliers
    elif row['Fixed or Variable'] == 'Variable':
        
        #Assigning multiplier variables for the given role, month, year, countries, program, study, trial stage, efficiency, etc. defined in the row
        ongoing_studies = ongoing_studies_finder(df, row['Month'], row['Year'])
        ongoing_molecules = ongoing_molecules_finder(df, row['Month'], row['Year'])
        trial_stage = row['Trial Stage']
        vendors = [row['Clinical Vendors'], row['Biometric Vendors']]
        reg_pot = True if row['Reg Pot'] == 'Yes' else False
        if trial_stage == '2/3': #temporary -- assume registrational potential is true if the study is in phase 2/3
            reg_pot = True
        countries = row['Countries']
        if countries == 'TBD':
            countries = 5 #Temporary -- if number of countries is TBD or blank in input table, assumes 5
        elif np.isnan(countries):
            countries = 0
        else:
            countries = int(countries)
        sites = row['Sites']
        if sites == 'TBD':
            sites = 1 #temporary -- value assigned to number of sites if data table is empty for given row
        elif sites == False:
            sites = 0
        else:
            sites = int(sites)
        program = row['Program']
        study_efficiency = study_efficiency_finder(df, trial_stage, program, row['Month'], row['Year'])
        efficiency = 1
        if study_efficiency:
            if trial_stage == '2/3' or trial_stage == '3':
                efficiency = efficiency * 0.6
        ole = True if row['Study or OLE'] == 'OLE' else False
        kol = row['KOL Demand']
        complexity = row['Trial Complexity']
        large_or_small = row['Small or Large Molecule']

        #Assigns base demand as trial phase demand
        demand = 1
        if trial_stage == 'Candidate ID':
            demand = row['Candidate ID']
            if row['Core or SEED'] == 'SEED':
                if row['SEED Support'] == 0:
                    demand = 0
        elif trial_stage == 'IND' or trial_stage == 'ind' or trial_stage == 'ind enabling' or trial_stage =='IND enabling' or trial_stage == 'IND Enabling':
            demand = row['IND Enabling']
            if row['Core or SEED'] == 'SEED':
                if row['SEED Support'] == 0:
                    demand = 0
        elif trial_stage == 'clin pharm' or trial_stage =='Clin Pharm' or trial_stage == 'clin' or trial_stage == '0' or trial_stage == 0:
            demand = row['Clin Pharm']
        elif trial_stage == '1' or trial_stage =='1a' or trial_stage == '1A' or trial_stage == '1 OLE':
            demand = row['Phase 1']
        elif trial_stage == '1b' or trial_stage == '1B' or trial_stage == '1b OLE' or trial_stage == '1B OLE':
            demand = row['Phase 1b']
        elif trial_stage == '2' or trial_stage =='2a' or trial_stage == '2b' or trial_stage =='1/2' or trial_stage == '2 OLE' or trial_stage == '1/2 OLE':
            demand = row['Phase 2'] 
        elif trial_stage == '2/3' or trial_stage == '2/3 OLE':
            demand = row['Phase 2/3'] 
        elif trial_stage == '3' or trial_stage == '3a' or trial_stage == '3b' or trial_stage == '3 OLE':
            demand = row['Phase 3']
        elif trial_stage == 'filing' or trial_stage == 'Filing':
            demand = row['Filing'] 
        elif trial_stage == '4' or trial_stage == '4 OLE':
            demand = row['Phase 4']

        #Multiplies base demand by complexity multiplier if applicable 
        d = demand
        if complexity == ('Low' or 'Normal'):
            d = demand * row['Complexity - Normal']
        elif complexity == 'Medium':
            d = demand * row['Complexity - Medium']
        elif complexity == 'Rare-High':
            d = demand * float(row['Complexity - High'])
        else:
            d = demand

        #Calculates demand (e) based on primary driver and multipliers determined by role, organized by Function, and in some cases Subfunction
        #Efficiency multiplied only to roles that specified to do so in resourcing summary
        #For program-driven roles, demand is allocated evenly among all studies in that program for that given role
        e = 1
        if row['Cost Number'] == 'Clinical Outsourcing Business Operations':
            if row['Role'] == 'COBO Study Lead': ### needs partnership multiplier
                vendor = vendors[0]
                e = d * vendor
            if row['Role'] == 'COBO Functional Lead': ### needs partnership multiplier
                vendor = vendors[1]
                e = d * vendor

        if row['Home Department'] == 'Regulatory & Clinical QA':
            if row['Role'] == 'Clinical Regulatory': ### Needs partnership multiplier
                e = d * efficiency
                if ongoing_studies > 3 and ongoing_studies < 7:
                    e = e * (((1.2 * (ongoing_studies - 3)) + 3) / ongoing_studies)
                elif ongoing_studies > 6:
                    e = e * ((3 + (1.2 * 3) + ((ongoing_studies - 6) * 1.4)) / ongoing_studies)
                else:
                    e = e
                if countries > 5:
                    e = e * 1.4
                if reg_pot:
                    e = e * row['Registrational Potential']
            if row['Role'] == 'CMC Regulatory':
                e = (d * efficiency * ongoing_molecules) / ongoing_studies
                if ongoing_studies > 3 and ongoing_studies < 7:
                    e = e * (((1.2 * (ongoing_studies - 3)) + 3) / ongoing_studies)
                elif ongoing_studies > 6:
                    e = e * ((3 + (1.2 * 3) + ((ongoing_studies - 6) * 1.4)) / ongoing_studies)
                else:
                    e = e
                if countries > 5:
                    e = e * 1.2
                if reg_pot:
                    e = e * 1.5
            if row['Role'] == 'Commercial Regulatory': ###Needs partnership multiplier 
                e = d * efficiency
                if countries > 5:
                    e = e * 1.2
            if row['Role'] == 'Clinical QA':
                e = d * efficiency
                if ongoing_studies > 3 and ongoing_studies < 7:
                    e = e * (((1.2 * (ongoing_studies - 3)) + 3) / ongoing_studies)
                elif ongoing_studies > 6:
                    e = e * ((3 + (1.2 * 3) + ((ongoing_studies - 6) * 1.4)) / ongoing_studies)
                else:
                    e = e
                if countries > 6:
                    e = e * 1.3
                if sum(vendors) > 6:
                    e = e * 1.2
                elif sum(vendors) > 12:
                    e = e * 1.4
                else:
                    e = e
                if sites > 10:
                    e = e * 1.2
                elif sites > 15:
                    e = e * 1.4
                elif sites > 20:
                    e = e * 1.5
                else:
                    e = e
            if row['Role'] == 'Regulatory Operations':
                e = d * efficiency
                if ongoing_studies > 3 and ongoing_studies < 7:
                    e = e * (((1.2 * (ongoing_studies - 3)) + 3) / ongoing_studies)
                elif ongoing_studies > 6:
                    e = e * ((3 + (1.2 * 3) + ((ongoing_studies - 6) * 1.4)) / ongoing_studies)
                else:
                    e = e
            if row['Role'] == 'Medical Writing':
                e = d * efficiency
                if ongoing_studies > 3 and ongoing_studies < 7:
                    e = e * (((1.2 * (ongoing_studies - 3)) + 3) / ongoing_studies)
                elif ongoing_studies > 6:
                    e = e * ((3 + (1.2 * 3) + ((ongoing_studies - 6) * 1.4)) / ongoing_studies)
                else:
                    e = e
            if row['Role'] == 'Compliance Training':
                e = employees / 100

        if row['Home Department'] == 'Biometrics':
            e = d
            if row['Role'] == 'BioStatistician - Project Lead':
                e = (e * ongoing_molecules) / ongoing_studies
            if row['Role'] == 'BioStatistician - Study Lead':
                e = e 
            if row['Role'] == 'Data Scientist - Project Lead': ### Needs outsourced multiplier
                e = (e * ongoing_molecules) / ongoing_studies
            if row['Role'] == 'Data Scientist - Study Lead': ### Needs outsourced multiplier
                e = e * efficiency

        if row['Home Department'] == 'Development Operations':
            if row['Cost Number'] == 'Clinical Data Management':
                e = d
                if row['Role'] == 'Data Management':
                    e = e * efficiency
                if row['Role'] == 'Data Management Program Lead':
                    e = (e * ongoing_molecules) / ongoing_studies
            if row['Cost Number'] == 'Clinical Operations':
                e = d 
                if row['Role'] == 'Clinical Program Manager':
                    e = (e * ongoing_molecules) 
                    if ongoing_studies > 1:
                        e = (e + (0.05 * ongoing_studies)) / ongoing_studies
                    else:
                        e = e / ongoing_studies
                if row['Role'] == 'Clinical Trial Manager':
                    e = e * efficiency
                if row['Role'] == 'Clinical Trial Associate':
                    e = (e * ongoing_molecules) / ongoing_studies 
                if row['Role'] == 'Clinical Research Associate':
                    e = e * efficiency * vendors[0] 

        if row['Home Department'] == 'Late Clinical, Medical Affairs, Pharmacovigilance':
            if row['Cost Number'] == 'Medical Affairs':
                e = d
                if row['Role'] == 'Medical Science Liaison - Low KOL': ### Add partnership multiplier
                    if row['KOL Demand'] == 'Low':
                        e = (e * ongoing_molecules) / ongoing_studies
                    else:
                        e = 0
                if row['Role'] == 'Medicial Science Liaison - High KOL': ### Add partnership multiplier
                    if row['KOL Demand'] == 'Medium' or row['KOL Demand'] == 'High':
                        e = (e * ongoing_molecules) / ongoing_studies
                    else:
                        e = 0
                if row['Role'] == 'Medical Affairs Medical Director':
                    e = (e * ongoing_molecules) / ongoing_studies
                if row['Role'] == 'Health Economics and Outcomes Research':
                    e = e * efficiency
                if row['Role'] == 'Medical Affairs - Other':
                    e = e * efficiency
            if row['Cost Number'] == 'Pharmacovigilance':
                e = d 
                if row['Role'] == 'Safety Science':
                    e = (e * row['Baseline Variable Demand']* ongoing_molecules) / ongoing_studies 
                if row['Role'] == 'PV Specialist':
                    e = (e * row['Baseline Variable Demand'] * ongoing_molecules) / ongoing_studies

        if row['Home Department'] == 'Early Clinical':
            e = d * row['Baseline Variable Demand']
            if row['Role'] == 'Early Medical Director':
                e = (e * ongoing_molecules) / ongoing_studies
            if row['Role'] == 'Early Clinical Science':
                e = (e * ongoing_molecules) / ongoing_studies
            if row['Role'] == 'Late Medical Director':
                e = (e * ongoing_molecules) / ongoing_studies
            if row['Role'] == 'Late Clinical Science':
                e = (e * ongoing_molecules) / ongoing_studies 
            if row['Role'] == 'Early Project Lead':
                e = (e * ongoing_molecules) / ongoing_studies
            if row['Role'] == 'Late Project Lead':
                e = (e * ongoing_molecules) / ongoing_studies

        if row['Home Department'] == 'Development Science':
            e = d 
            if row['Cost Number'] == 'DMPK':
                if row['Role'] == 'DMPK Bioanalytical Sciences - SM':
                    e = e * efficiency
                    if large_or_small == 'Large Molecule':
                        e = 0
                if row['Role'] == 'DMPK Bioanalytical Sciences - LM':
                    e = e * efficiency
                    if large_or_small == 'Small Molecule':
                        e = 0

            if row['Role'] == 'Clinical Pharmacologist':
                e = e * efficiency
                if complexity == 'High-Rare' or complexity == 'High' or complexity == 'Rare':
                    if trial_stage == 'clin pharm' or trial_stage =='Clin Pharm' or trial_stage == 'clin' or trial_stage == '0' or trial_stage == 0:
                        e = e * 2
                    else:
                        e = e
            if row['Role'] == 'Toxicology (variable)':
                e = e * efficiency 
            if row['Role'] == 'Pathology (variable)':
                e = e * efficiency
            if row['Role'] == 'Non-Clinical Operations (variable)':
                e = e * efficiency
            if row['Role'] == 'DMPK (variable)':
                e = e * efficiency

        if row['Home Department'] == 'Translational Sciences':
            e = d
            if row['Role'] == 'PreClinical BioMarker Scientist':
                e = (e * ongoing_molecules) / ongoing_studies
            if row['Role'] == 'PreClinical BioMarker Operation Specialist':
                e = e
            if row['Role'] == 'PreClinical BioMarker Technical Specialist':
                e = e
            if row['Role'] == 'Biosample Operations Specialist':
                e = e
            if row['Role'] == 'Biomarker Operations Specialist':
                e = (e * ongoing_molecules) / ongoing_studies
            if row['Role'] == 'Biorepository Specialist (variable)':
                e = (e * ongoing_molecules) / ongoing_studies
            if row['Role'] == 'Clinical Biomarker Scientist':
                e = e * efficiency

        #Applies OLE multiplier if study is an OLE
        if ole:
            e = e * 0.5

        #Fills in appropriate demand (e) for each study milestone for row's specific role (before applying SEED Factor)
        if row['Previous Milestone'] == 'ramp_up':
            row['Demand'] = e * row['Study Start'] * 0.15
        elif row['Previous Milestone'] == 'study_start':
            row['Demand'] = e * row['Study Start']
            if trial_stage == 'Filing':
                row['Demand'] = e * row['Study Start'] * 0.5
        elif row['Previous Milestone'] == 'fpi':
            row['Demand'] = e * row['FPI']
            if trial_stage == 'Filing':
                row['Demand'] = e * row['FPI'] * 0.5
        elif row['Previous Milestone'] == 'lpi':
            row['Demand'] = e * row['LPI']
            if trial_stage == 'Filing':
                row['Demand'] = e * row['LPI'] * 0.5
        elif row['Previous Milestone'] == 'lpo':
            row['Demand'] = e * row['LPO']
            if trial_stage == 'Filing':
                row['Demand'] = e * row['LPO'] * 0.5
        elif row['Previous Milestone'] == 'dbl':
            row['Demand'] = e * row['DBL']
            if trial_stage == 'Filing':
                row['Demand'] = e * row['DBL'] * 0.5
        elif row['Previous Milestone'] == 'top_line_results':
            row['Demand'] = e * row['Top Line Results']
        elif row['Previous Milestone'] == 'csr':
            row['Demand'] = e * row['CSR']
        
        row['All-in Demand'] = row['Demand']
        row['PTS Demand'] = row['Demand'] * row['PTS']
        
    if row['Study Number'] == 'Partner Demand':
        if row['Fixed or Variable'] == 'Placed':
            if row['Role'] == 'LRRK2 Partner Fixed Headcount':
                row['All-in Demand'] = row['Fixed Demand']
                row['PTS Demand'] = row['Fixed Demand']
                row['Program'] = 'LRRK2'
            if row['Role'] == 'RIPK1 Partner Fixed Headcount':
                row['All-in Demand'] = row['Fixed Demand']
                row['PTS Demand'] = row['Fixed Demand']
                row['Program'] = 'RIPK1'
        else:
            row['All-in Demand'] = 0
            row['PTS Demand'] = 0
        
        
    
        
def fte_generator(lrp_data):
    print("process started output")

    output_timeline = output_timeline_maker(lrp_data)
    
    ### Filter to run certain studies at a time:
    #output_timeline = output_timeline[output_timeline['Study Number'] == 'DNLI-E-0003'] 
    resourcing_summary = pd.read_csv('Resourcing Summary Assumptions.csv')
    resourcing_summary = resourcing_summary.iloc[0:72]
    ### Filter to run a single role:
    #resourcing_summary = resourcing_summary[resourcing_summary['Role'] == 'Compliance Training'] 
    ### Filter to run a single subfunction:
    #resourcing_summary = resourcing_summary[resourcing_summary['Home Department'] == 'Regulatory & Clinical QA'] 
    ### Filter to run only fixed or variable roles
    #resourcing_summary = resourcing_summary[resourcing_summary['Fixed or Variable'] == 'Variable']
    
    #Create output data structure with one row per role per month per study
    df = output_timeline.assign(key=1).merge(resourcing_summary.assign(key=1), how='outer', on='key')
    
    partner = 'Non-partnered' #Current assumption is all studies are non-partnered. If later we want to distinguish partnership on a per-study basis, that needs to be an added column in the "LRP Data" input file
    sourcing = 'Outsourced' #Current assumption is all studies are outsourced. If later we want to distinguish sourcing on a per-study basis, that needs to be an added column in the "LRP Data" input file
    #if partner == 'Partnered':  -- add partnership rules here ex: if a study is partnered, then it's insoruced.
        #sourcing = 
    device = False #temporary  -- device toggles go here. Device toggles not currently used
    employees = 350 #temporary -- number of Denali employees assumed to be 350 constant. This maybe something that needs to be coded into the algorithm in the future in terms of multiplying by a growth factor each year.

    #Add additional columns to output table
    df['Partnered or Non-partnered'] = partner
    df['Insourced or Outsourced'] = sourcing
    
    #These following columns will be calculated 
    df['Demand'] = 0
    df['All-in Demand'] = 0
    df['PTS Demand'] = 0

    #Iterate through each row of output table and fill in the All-in Demand and PTS Demand column
    rows = []
    for index,row in df.iterrows():
        d = row.to_dict()
        fte_calculator(d, output_timeline, partner, employees)
        rows.append(d)
    output = pd.DataFrame(rows)
    
    #Add Date column in the format MM/YYYY
    output['mm'] = output['Month']
    output['mm']= output['mm'].replace({1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12'})
    output['yyyy'] = output['Year'].astype(str)
    output['Date'] = output['mm'] + '/' + output['yyyy']
    
    #Return output with specified columns in specified order
    return output[['Program', 'Study Number', 'Role', 'Business Unit', 'Home Department', 'Cost Number', 'Fixed or Variable', 'Efficiency', 'Partnered or Non-partnered', 'Insourced or Outsourced', 'Previous Milestone', 'Core or SEED','Month', 'Year', 'Date', 'All-in Demand', 'PTS Demand']]

pd.set_option("display.max_columns", None)


# In[417]:


#To run and save as an excel file

fte_generator(lrp_data).to_excel('FTE_GOAL_OUPTUT_2021Aug23.xlsx')


# In[ ]:





# In[ ]:





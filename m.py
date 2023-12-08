from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)

if not os.path.exists("uploads"):

    os.makedirs("uploads")
if not os.path.exists("download_temp"):
    os.makedirs("download_temp")

def process_csv(file_path):
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, sheet_name="Data")
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        # Handle other file formats if needed
        return None

    nan_columns = df.columns[df.isna().all()].tolist()

    (df.isna().sum())

    for column in df.columns:
        (f"{column}: {df[column].unique()}")

    if not nan_columns:
        return None
    return nan_columns



def fill_nan(file_path, column_values):
    print("\n\n\n"+file_path+"\n\n\n")
    input_file_path = "uploads/" + file_path
    output_file_path = "download_temp/" + file_path.replace(".xlsx", "_modified.xlsx")

    with pd.ExcelFile(input_file_path) as xls:
        df = pd.read_excel(xls, sheet_name="Data")

        print("Columns in the DataFrame:", df.columns)
        print("Columns to fill:", column_values)

        for column, value in column_values.items():
            print(f"Filling NaN values in column {column} with value {value}")
            df[column] = df[column].fillna(value)

    df.to_excel(output_file_path, index=False, sheet_name='Data')

    return output_file_path


def formater(file_path):
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name="Data")
        # Handle None columns
        df.dropna(thresh=3, inplace=True)

        df['File Number'] = df['Account'].astype(str) + df['Abbreviation']

        headers=['BilledTransactionsId', 'PracticeName', 'DOWNLOAD', 'DUPECHECK',
                'Docket#', 'OrderID/Acc#', 'TransactionNumber', 'Account',
                'Abbadox_ApptID', 'PatientName', 'BirthDate', 'Sex', 'PatientAddress',
                'PatientCity', 'PatientState', 'PatientZip', 'PatientPhone', 'InsCode1',
                'Insurance1', 'CaseManager', 'ARClass', 'InsuranceAddress',
                'InsuranceAddress2', 'InsuranceCity', 'InsuranceState', 'InsuranceZip',
                'InsurancePhone', 'InsuranceFax', 'PostingDate', 'DOS', 'DOI',
                'ChargesBaseCPT', 'ChargesCPTCode', 'ChargesCPTDescription', 'Modality',
                'Diag', 'Provider', 'ProviderName', 'RefCode', 'RefName',
                'AttorneyCode', 'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2',
                'AttorneyCity', 'AttorneyState', 'AttorneyZip', 'AttorneyPhone',
                'AttorneyFax', 'Plc', 'Balance', 'Fund', 'Status', 'Lien', 'Bill',
                'Report', 'Saba s Notes', 'Notes', 'Abbreviation', 'File Opened', 'P&L',
                'Referral Source', 'Provider Invoice Number', 'Cogs Multiplier',
                'Date Paid', 'Payment Status', 'File Number']
        df.columns=headers

        df[['Client Last Name', 'Client First Name']] = df['PatientName'].str.split(', ', n=1, expand=True)

        headers=['BilledTransactionsId', 'PracticeName', 'DOWNLOAD', 'DUPECHECK',
                'Docket#', 'OrderID/Acc#', 'TransactionNumber', 'Account',
                'Abbadox_ApptID', 'PatientName', 'Client DOB ', 'Sex', 'PatientAddress',
                'PatientCity', 'PatientState', 'PatientZip', 'PatientPhone', 'InsCode1',
                'Insurance1', 'CaseManager', 'ARClass', 'InsuranceAddress',
                'InsuranceAddress2', 'InsuranceCity', 'InsuranceState', 'InsuranceZip',
                'InsurancePhone', 'InsuranceFax', 'PostingDate', 'DOS', 'Date of Loss ',
                'ChargesBaseCPT', 'ChargesCPTCode', 'ChargesCPTDescription', 'Modality',
                'Diag', 'Provider', 'ProviderName', 'RefCode', 'RefName',
                'AttorneyCode', 'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2',
                'AttorneyCity', 'AttorneyState', 'AttorneyZip', 'AttorneyPhone',
                'AttorneyFax', 'Plc', 'Balance', 'Fund', 'Status', 'Lien', 'Bill',
                'Report', 'Saba s Notes', 'Notes', 'Abbreviation', 'File Opened', 'P&L',
                'Referral Source', 'Provider Invoice Number', 'Cogs Multiplier',
                'Date Paid', 'Payment Status', 'File Number', 'Client Last Name',
                'Client First Name']
        df.columns=headers
        
        df['Language'] = 'English'

        from datetime import datetime 
        df['Client DOB '] = pd.to_datetime(df['Client DOB '])
        today_date = datetime(2023, 12, 6)
        df['age'] = (today_date - df['Client DOB ']).dt.days // 365
        df['Minor'] = df['age'] < 18
        df['Minor'] = df['Minor'].map({True: 'Yes', False: 'No'})
        df = df.drop('age', axis=1)

        headers=['BilledTransactionsId', 'PracticeName', 'DOWNLOAD', 'DUPECHECK',
                'Docket#', 'OrderID/Acc#', 'TransactionNumber', 'Account',
                'Abbadox_ApptID', 'PatientName', 'Client DOB ', 'Sex', 'PatientAddress',
                'PatientCity', 'PatientState', 'PatientZip', 'Client Phone ', 'InsCode1',
                'Insurance1', 'CaseManager', 'ARClass', 'InsuranceAddress',
                'InsuranceAddress2', 'InsuranceCity', 'InsuranceState', 'InsuranceZip',
                'InsurancePhone', 'InsuranceFax', 'PostingDate', 'DOS', 'Date of Loss ',
                'ChargesBaseCPT', 'ChargesCPTCode', 'ChargesCPTDescription', 'Modality',
                'Diag', 'Provider', 'ProviderName', 'RefCode', 'RefName',
                'AttorneyCode', 'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2',
                'AttorneyCity', 'AttorneyState', 'AttorneyZip', 'AttorneyPhone',
                'AttorneyFax', 'Plc', 'Balance', 'Fund', 'Status', 'Lien', 'Bill',
                'Report', 'Saba s Notes', 'Notes', 'Abbreviation', 'File Opened', 'P&L',
                'Referral Source', 'Provider Invoice Number', 'Cogs Multiplier',
                'Date Paid', 'Payment Status', 'File Number', 'Client Last Name',
                'Client First Name', 'Language', 'Minor']
        df.columns=headers

        df['Client Email '] = ' '

        headers=['BilledTransactionsId', 'PracticeName', 'DOWNLOAD', 'DUPECHECK',
            'Docket Number', 'OrderID/Acc#', 'TransactionNumber', 'Account',
            'Abbadox_ApptID', 'PatientName', 'Client DOB ', 'Sex', 'PatientAddress',
            'PatientCity', 'PatientState', 'PatientZip', 'Client Phone ',
            'InsCode1', 'Law Firm', 'CaseManager', 'ARClass', 'InsuranceAddress',
            'InsuranceAddress2', 'InsuranceCity', 'InsuranceState', 'InsuranceZip',
            'InsurancePhone', 'InsuranceFax', 'PostingDate', 'DOS', 'Date of Loss ',
            'ChargesBaseCPT', 'ChargesCPTCode', 'ChargesCPTDescription', 'Modality',
            'Diag', 'Provider', 'ProviderName', 'RefCode', 'RefName',
            'AttorneyCode', 'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2',
            'AttorneyCity', 'AttorneyState', 'AttorneyZip', 'AttorneyPhone',
            'AttorneyFax', 'Plc', 'Balance', 'Fund', 'Status', 'Lien', 'Bill',
            'Report', 'Saba s Notes', 'Notes', 'Abbreviation', 'File Opened', 'P&L',
            'Referral Source', 'Provider Invoice Number', 'Cogs Multiplier',
            'Date Paid', 'Payment Status', 'File Number', 'Client Last Name',
            'Client First Name', 'Language', 'Minor', 'Client Email ']
        df.columns=headers

        df['Attorney '] = ' '

        headers=['BilledTransactionsId', 'PracticeName', 'DOWNLOAD', 'DUPECHECK',
            'Docket Number', 'OrderID/Acc#', 'TransactionNumber', 'Law Firm File Number',
            'Abbadox_ApptID', 'PatientName', 'Client DOB ', 'Sex', 'PatientAddress',
            'PatientCity', 'PatientState', 'PatientZip', 'Client Phone ',
            'InsCode1', 'Law Firm', 'CaseManager', 'ARClass', 'Law Firm Address ',
            'Law Firm Suite', 'Law Firm City', 'Law Firm State', 'Law Firm ZIP',
            'Law Firm Phone', 'Law Firm Fax', 'PostingDate', 'DOS', 'Date of Loss ',
            'ChargesBaseCPT', 'ChargesCPTCode', 'ChargesCPTDescription', 'Modality',
            'Diag', 'Provider', 'ProviderName', 'RefCode', 'RefName',
            'AttorneyCode', 'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2',
            'AttorneyCity', 'AttorneyState', 'AttorneyZip', 'AttorneyPhone',
            'AttorneyFax', 'Plc', 'Balance', 'Fund', 'Status', 'Lien', 'Bill',
            'Report', 'Saba s Notes', 'Notes', 'Abbreviation', 'File Opened', 'P&L',
            'Referral Source', 'Provider Invoice Number', 'Cogs Multiplier',
            'Date Paid', 'Payment Status', 'File Number', 'Client Last Name',
            'Client First Name', 'Language', 'Minor', 'Client Email ', 'Attorney ']
        df.columns=headers

        df['Statuser'] = "Provider-" + df['Abbreviation']
        df['Case Manager'] = "Jackie Williams"
        df['Market Manager'] = "Nate Ormond"
        df['Active Care'] = "No"

        headers=['BilledTransactionsId', 'PracticeName', 'DOWNLOAD', 'DUPECHECK',
            'Docket Number', 'OrderID/Acc#', 'TransactionNumber',
            'Law Firm File Number', 'Abbadox_ApptID', 'PatientName', 'Client DOB ',
            'Sex', 'Client Address1', 'Client Address - City ',
            'Clinet Address - State', 'Client Address - ZIP', 'Client Phone ',
            'InsCode1', 'Law Firm', 'CaseManager', 'ARClass', 'Law Firm Address ',
            'Law Firm Suite', 'Law Firm City', 'Law Firm State', 'Law Firm ZIP',
            'Law Firm Phone', 'Law Firm Fax', 'PostingDate', 'DOS', 'Date of Loss ',
            'ChargesBaseCPT', 'ChargesCPTCode', 'ChargesCPTDescription', 'Modality',
            'Diag', 'Provider', 'ProviderName', 'RefCode', 'Referring Physician',
            'AttorneyCode', 'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2',
            'AttorneyCity', 'AttorneyState', 'AttorneyZip', 'AttorneyPhone',
            'AttorneyFax', 'Plc', 'Balance', 'Fund', 'Status', 'Lien', 'Bill',
            'Report', 'Saba s Notes', 'Notes', 'Abbreviation', 'File Opened',
            'P & L', 'Referral Source', 'Provider Invoice Number',
            'Cogs Multiplier', 'Date Paid', 'Payment Status', 'File Number',
            'Client Last Name', 'Client First Name', 'Language', 'Minor',
            'Client Email ', 'Attorney ', 'Statuser', 'Case Manager ',
                'Market Manager', 'Active Care']
        df.columns=headers

        df['Client Address2 '] = ' '
        df['Record Status'] = "Active"
        df['Statute of Limitations'] = ' '
        df['File Group'] = ' '
        df['Note Type'] = ' '
        df['Provider'] = ' '
        df['Date'] = ' '
        df['Time'] = ' '
        df['Priority'] = ' '
        df['Note'] = ' '
        df['Next Date of Activity'] = ' '
        df['Next Activity Type'] = ' '
        df['RemindTo'] = ' '

        headers=['BilledTransactionsId', 'Organization', 'DOWNLOAD', 'DUPECHECK',
            'Docket Number', 'OrderID/Acc#', 'TransactionNumber',
            'Law Firm File Number', 'Abbadox_ApptID', 'PatientName', 'Client DOB ',
            'Sex', 'Client Address1', 'Client Address - City ',
            'Clinet Address - State', 'Client Address - ZIP', 'Client Phone ',
            'InsCode1', 'Law Firm', 'CaseManager', 'ARClass', 'Law Firm Address ',
            'Law Firm Suite', 'Law Firm City', 'Law Firm State', 'Law Firm ZIP',
            'Law Firm Phone', 'Law Firm Fax', 'PostingDate', 'Invoice Date', 'Date of Loss ',
            'ChargesBaseCPT', 'ChargesCPTCode', 'ChargesCPTDescription', 'Modality',
            'Diag', 'Provider', 'Provider Name', 'RefCode', 'Referring Physician',
            'AttorneyCode', 'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2',
            'AttorneyCity', 'AttorneyState', 'AttorneyZip', 'AttorneyPhone',
            'AttorneyFax', 'Location', 'Balance', 'Fund', 'Status', 'Lien', 'Bill',
            'Report', 'Saba s Notes', 'Notes', 'Abbreviation', 'File Opened',
            'P & L', 'Referral Source', 'Provider Invoice Number',
            'Cogs Multiplier', 'Date Paid', 'Payment Status', 'File Number',
            'Client Last Name', 'Client First Name', 'Language', 'Minor',
            'Client Email ', 'Attorney ', 'Statuser', 'Case Manager ',
            'Market Manager', 'Active Care', 'Client Address2 ',
            'Record Status', 'Statute of Limitations', 'File Group', 'Note Type',
            'Date', 'Time', 'Priority', 'Note', 'Next Date of Activity',
            'Next Activity Type', 'RemindTo']
        df.columns=headers

        df['In Network'] = "Yes"
        df['Lock Invoice'] = "Yes"
        df['Out of Network Fee'] = '0'
        df['Surgical Invoice'] = "No"

        headers=['BilledTransactionsId', 'Organization', 'DOWNLOAD', 'DUPECHECK',
            'Docket Number', 'OrderID/Acc#', 'TransactionNumber',
            'Law Firm File Number', 'Appt ID', 'PatientName', 'Client DOB ',
            'Sex', 'Client Address1', 'Client Address - City ',
            'Clinet Address - State', 'Client Address - ZIP', 'Client Phone ',
            'InsCode1', 'Law Firm', 'CaseManager', 'ARClass', 'Law Firm Address ',
            'Law Firm Suite', 'Law Firm City', 'Law Firm State', 'Law Firm ZIP',
            'Law Firm Phone', 'Law Firm Fax', 'PostingDate', 'Invoice Date',
            'Date of Loss ', 'ChargesBaseCPT', 'ChargesCPTCode',
            'Notes', 'Modality', 'Diag', 'Provider',
            'Provider Name', 'RefCode', 'Referring Physician', 'AttorneyCode',
            'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2', 'AttorneyCity',
            'AttorneyState', 'AttorneyZip', 'AttorneyPhone', 'AttorneyFax',
            'Location', 'Amount Billed', 'Fund', 'Status', 'Lien', 'Bill', 'Report',
            'Saba s Notes', 'Notes', 'Abbreviation', 'File Opened', 'P & L',
            'Referral Source', 'Provider Invoice Number', 'Cogs Multiplier',
            'Date Paid', 'Payment Status', 'File Number', 'Client Last Name',
            'Client First Name', 'Language', 'Minor', 'Client Email ', 'Attorney ',
            'Statuser', 'Case Manager ', 'Market Manager',
            'Active Care', 'Client Address2 ', 'Record Status',
            'Statute of Limitations', 'File Group', 'Note Type', 'Date', 'Time',
            'Priority', 'Note', 'Next Date of Activity', 'Next Activity Type',
            'RemindTo', 'In Network', 'Lock Invoice', 'Out of Network Fee',
            'Surgical Invoice']
        df.columns=headers

        df['Reimbursement Rate'] = (df['Fund'] * 10) / df['Amount Billed']
        df['Total Due Provider'] = (df['Fund'] * 10)

        df['Settlement Value'] = df['Amount Billed'].copy()

        df['Funder Invoice'] = "Yes"

        headers=['BilledTransactionsId', 'Organization', 'DOWNLOAD', 'DUPECHECK',
            'Docket Number', 'OrderID/Acc#', 'TransactionNumber',
            'Law Firm File Number', 'Appt ID', 'PatientName', 'Client DOB ', 'Sex',
            'Client Address1', 'Client Address - City ', 'Clinet Address - State',
            'Client Address - ZIP', 'Client Phone ', 'InsCode1', 'Law Firm',
            'CaseManager', 'ARClass', 'Law Firm Address ', 'Law Firm Suite',
            'Law Firm City', 'Law Firm State', 'Law Firm ZIP', 'Law Firm Phone',
            'Law Firm Fax', 'PostingDate', 'Invoice Date', 'Date of Loss ',
            'ChargesBaseCPT', 'ChargesCPTCode', 'Notes', 'Modality', 'Diag',
            'Provider', 'Provider Name', 'RefCode', 'Referring Physician',
            'AttorneyCode', 'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2',
            'AttorneyCity', 'AttorneyState', 'AttorneyZip', 'AttorneyPhone',
            'AttorneyFax', 'Location', 'Amount Billed', 'Provider Settlement Value', 'Status', 'Lien',
            'Bill', 'Report', 'Saba s Notes', 'Notes', 'Abbreviation',
            'File Opened', 'P & L', 'Referral Source', 'Provider Invoice Number',
            'Cogs Multiplier', 'Date Paid', 'Payment Status', 'File Number',
            'Client Last Name', 'Client First Name', 'Language', 'Minor',
            'Client Email ', 'Attorney ', 'Statuser', 'Case Manager ',
            'Market Manager', 'Active Care', 'Client Address2 ', 'Record Status',
            'Statute of Limitations', 'File Group', 'Note Type', 'Date', 'Time',
            'Priority', 'Note', 'Next Date of Activity', 'Next Activity Type',
            'RemindTo', 'In Network', 'Lock Invoice', 'Out of Network Fee',
            'Surgical Invoice', 'Reimbursement Rate', 'Total Due Provider',
            'Settlement Value', 'Funder Invoice']
        df.columns=headers

        df['Balance Due'] = (df['Provider Settlement Value'] * 10)
        df['Amount Paid'] = (df['Provider Settlement Value'] * 10)

        df['Payment Method'] = "Wire Transfer"

        headers=['BilledTransactionsId', 'Organization', 'DOWNLOAD', 'DUPECHECK',
            'Docket Number', 'OrderID/Acc#', 'TransactionNumber',
            'Law Firm File Number', 'Appt ID', 'PatientName', 'Client DOB ', 'Sex',
            'Client Address1', 'Client Address - City ', 'Clinet Address - State',
            'Client Address - ZIP', 'Client Phone ', 'InsCode1', 'Law Firm',
            'CaseManager', 'ARClass', 'Law Firm Address ', 'Law Firm Suite',
            'Law Firm City', 'Law Firm State', 'Law Firm ZIP', 'Law Firm Phone',
            'Law Firm Fax', 'PostingDate', 'Invoice Date', 'Date of Loss ',
            'ChargesBaseCPT', 'CPTCode', 'Notes', 'Modality', 'Diag',
            'Provider', 'Provider Name', 'RefCode', 'Referring Physician',
            'AttorneyCode', 'AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2',
            'AttorneyCity', 'AttorneyState', 'AttorneyZip', 'AttorneyPhone',
            'AttorneyFax', 'Location', 'Amount Billed', 'Provider Settlement Value',
            'Status', 'Lien', 'Bill', 'Report', 'Saba s Notes', 'Notes',
            'Abbreviation', 'File Opened', 'P & L', 'Referral Source',
            'Provider Invoice Number', 'Cogs Multiplier', 'Date Paid',
            'Payment Status', 'File Number', 'Client Last Name',
            'Client First Name', 'Language', 'Minor', 'Client Email ', 'Attorney ',
            'Statuser', 'Case Manager ', 'Market Manager', 'Active Care',
            'Client Address2 ', 'Record Status', 'Statute of Limitations',
            'File Group', 'Note Type', 'Date', 'Time', 'Priority', 'Note',
            'Next Date of Activity', 'Next Activity Type', 'RemindTo', 'In Network',
            'Lock Invoice', 'Out of Network Fee', 'Surgical Invoice',
            'Reimbursement Rate', 'Total Due Provider', 'Settlement Value',
            'Funder Invoice', 'Balance Due', 'Amount Paid', 'Payment Method']
        df.columns=headers

        df['Check Number'] = ' '
        df['Insurance Company'] = ' '
        df['Claim Number'] = ' '
        df['Types of Insurance'] = ' '
        df['Policy Limits'] = ' '
        df['Claim Adjuster'] = ' '
        df['Adjuster Phone'] = ' '
        df['Adjuster Email'] = ' '
        df['Adjuster Fax'] = ' '
        df[' Notes '] = ' '
        df['Date Signed'] = ' '
        df['Amount '] = ' '
        df['Auth Type'] = ' '
        df['UCC Filed'] = "Yes"
        df['Date UCC Filed'] = ' '
        df['Signed Lien'] = "Yes"
        df['HIPAA Signed'] = "Yes"
        df['Intake Form'] = "No"

        df['Date of Service'] = df['Invoice Date'].copy()

        column_to_drop = ['AttorneyName', 'AttorneyAddress1', 'AttorneyAddress2', 'AttorneyCity',
            'AttorneyState', 'AttorneyZip', 'AttorneyPhone', 'AttorneyFax']
        df = df.drop(column_to_drop, axis=1)

        column_to_drop = 'PostingDate'
        df = df.drop(column_to_drop, axis=1)

        column_to_drop = 'ChargesBaseCPT'
        df = df.drop(column_to_drop, axis=1)

        column_to_drop = 'Diag'
        df = df.drop(column_to_drop, axis=1)

        column_to_drop = 'RefCode'
        df = df.drop(column_to_drop, axis=1)

        column_to_drop = ['BilledTransactionsId', 'DOWNLOAD', 'DUPECHECK', 'OrderID/Acc#',
            'TransactionNumber', 'PatientName', 'Sex', 'InsCode1','CaseManager','ARClass',]
        df = df.drop(column_to_drop, axis=1)

        headers=['Organization', 'Docket Number', 'Law Firm File Number', 'Appt ID',
            'Client DOB ', 'Client Address1', 'Client Address - City ',
            'Clinet Address - State', 'Client Address - ZIP', 'Client Phone ',
            'Law Firm', 'Law Firm Address ', 'Law Firm Suite', 'Law Firm City',
            'Law Firm State', 'Law Firm ZIP', 'Law Firm Phone', 'Law Firm Fax',
            'Invoice Date', 'Date of Loss ', 'CPTCode', 'Notes  ', 'Modality',
            'Provider', 'Provider Name', 'Referring Physician', 'AttorneyCode',
            'Location', 'Amount Billed', 'Provider Settlement Value', 'Status',
            'Lien', 'Bill', 'Report', 'Saba s Notes', 'notes', 'Abbreviation',
            'File Opened', 'P & L', 'Referral Source', 'Provider Invoice Number',
            'Cogs Multiplier', 'Date Paid', 'Payment Status', 'File Number',
            'Client Last Name', 'Client First Name', 'Language', 'Minor',
            'Client Email ', 'Attorney ', 'Statuser', 'Case Manager ',
            'Market Manager', 'Active Care', 'Client Address2 ', 'Record Status',
            'Statute of Limitations', 'File Group', 'Note Type', 'Date', 'Time',
            'Priority', 'Note', 'Next Date of Activity', 'Next Activity Type',
            'RemindTo', 'In Network', 'Lock Invoice', 'Out of Network Fee',
            'Surgical Invoice', 'Reimbursement Rate', 'Total Due Provider',
            'Settlement Value', 'Funder Invoice', 'Balance Due', 'Amount Paid',
            'Payment Method', 'Check Number', 'Insurance Company', 'Claim Number',
            'Types of Insurance', 'Policy Limits', 'Claim Adjuster',
            'Adjuster Phone', 'Adjuster Email', 'Adjuster Fax', ' Notes ',
            'Date Signed', 'Amount ', 'Auth Type', 'UCC Filed', 'Date UCC Filed',
            'Signed Lien', 'HIPAA Signed', 'Intake Form', 'Date of Service']
        df.columns=headers

        column_to_drop =['Bill', 'Report', 'Saba s Notes', 'notes']
        df = df.drop(column_to_drop, axis=1)

        desired_order = ['File Number', 'File Opened', 'Client First Name','Client Last Name','Client DOB ','Date of Loss ','Language',
                                    'Minor','Client Phone ','Client Email ','Law Firm','Docket Number','Attorney ','Law Firm File Number', 'Law Firm Address ',
                                    'Law Firm Suite', 'Law Firm City','Law Firm State', 'Law Firm ZIP', 'Law Firm Phone', 'Law Firm Fax','Statuser', 'Case Manager ',
                                    'Market Manager','Active Care', 'Client Address1','Client Address2 ', 'Client Address - City ', 'Clinet Address - State', 'Client Address - ZIP',
                                    'P & L', 'Referring Physician','Referral Source', 'Record Status', 'Statute of Limitations', 'File Group','Note Type', 'Provider','Date', 'Time', 'Priority', 'Note',
                                    'Next Date of Activity', 'Next Activity Type', 'RemindTo', 'Location','Organization','Provider Name','In Network','Invoice Date',
                                    'Lock Invoice', 'Provider Invoice Number', 'Out of Network Fee', 'Surgical Invoice','Notes  ','Date of Service','CPTCode','Appt ID',
                                    'Modality','Amount Billed','Reimbursement Rate', 'Total Due Provider', 'Settlement Value', 'Provider Settlement Value', 'Funder Invoice', 'Date Paid',
                                    'Balance Due', 'Amount Paid', 'Payment Method', 'Check Number', 'Payment Status', 'Insurance Company',
                                'Claim Number', 'Types of Insurance', 'Policy Limits', 'Claim Adjuster',
                                'Adjuster Phone', 'Adjuster Email', 'Adjuster Fax', ' Notes ',
                                'Date Signed', 'Amount ', 'Auth Type', 'UCC Filed', 'Date UCC Filed',
                                'Signed Lien', 'HIPAA Signed', 'Intake Form']
        df = df[desired_order]
        df.replace(' ', np.nan, inplace=True)
        # Create the 'downloads' directory if it doesn't exist
        #os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

        # Save modified DataFrame back to Excel file
        #modified_file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], f"{os.path.splitext(file}_modified.xlsx")
        df.to_excel(file_path, index=False,sheet_name="Data")
        
@app.route('/', methods=['GET', 'POST'])
def process_files():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        file_nan_dict = {}
        file_index = 0

        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join("uploads", filename)
                file.save(file_path)
                formater(file_path)

                nan_columns = process_csv(file_path)
                print(f"File: {filename}, Empty Columns: {nan_columns}")

                if nan_columns is not None and len(nan_columns) != 0:
                    file_nan_dict[file_index] = {"columns": nan_columns, "filename": filename, "index": file_index}
                    file_index += 1

        if file_nan_dict:
            return render_template('form.html', data=file_nan_dict)
        else:
            return "No completely empty columns found"

    return render_template('upload.html')



@app.route('/download_file', methods=['POST'])
def download_single_file():
    selected_filename = request.form.get('selected_filename')
    print(f"Selected Filename: {selected_filename}")
    fill_nan_values()

    original_file_path = os.path.join("uploads", selected_filename)
    modified_file_path = os.path.join("download_temp", selected_filename.replace(".xlsx", "_modified.xlsx"))

    if os.path.exists(modified_file_path):
        print("Sending modified file.")
        return send_file(modified_file_path, as_attachment=True)
    else:
        return "File not found"


@app.route('/fill_nan', methods=['POST'])
def fill_nan_values():
    file_path = request.form
    fnames = {}
    for i in file_path:
        if i.startswith("filename_"):
            fnames[i] = file_path[i]

    nandata = {}
    for i in fnames:
        findex = i.replace("filename_", "")
        file_nan = {}
        for j in file_path:
            if j.startswith(f"col_{findex}_"):
                file_nan[j.replace(f"col_{findex}_", "")] = file_path[j]
        nandata[findex] = file_nan

    files = []
    for i in nandata:
        filepath = "uploads\\" + fnames[f"filename_{i}"]
        if nandata[i]:
            column_values = nandata[i]
            modified_file = fill_nan(fnames["filename_" + str(i)], column_values)
            files.append(modified_file)

    if len(files) == 1:
        # If there's only one file, send it as a single file download
        return send_file(files[0], as_attachment=True, download_name=os.path.basename(files[0]))

    # If there are multiple files, create a zip archive and send it
    zip_filename = 'modified_files.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for file in files:
            zip_file.write(file, os.path.basename(file))

    # Send the ZIP file as a response
    return send_file(zip_filename, as_attachment=True, download_name='download.zip')

@app.route('/settings', methods=['POST'])
def settings():
    try:
        # Check for the correct field name 'files[]'
        if 'refFile' not in request.files:
            return "No file part in the request", 400

        files = request.files['refFile']
        return str(files)
        # Rest of your route code...
    except Exception as e:
        print(e)
        return f"An error occurred: {str(e)}", 500



if __name__ == '__main__':
    app.run(debug=True)

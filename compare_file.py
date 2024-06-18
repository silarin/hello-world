# This script compares 2 Excel files of the same format for new additions and changes across both files.
# Use pandas.read_excel() method to parse Excel files into a dict of DataFrames (df1 and df2).
import os
import gc
import glob
import datetime
import shutil as sh
import pandas as pd
import numpy as np

file1 = 'file1.xlsx'
file2 = 'file2.xlsx'
output_file = 'output.xlsx'

try:
    # Read file1 and file2 into a DataFrame.
    df1 = pd.read_excel(file1, sheet_name=None)
    df2 = pd.read_excel(file2, sheet_name=None)
    
except Exception as e:
    # Print error and stop program execution.
    print('File open FAILED.\r\n' + str(e))
    quit()
    
try:
    # Create file descriptor with ExcelWriter and setup the date formats.
    writer = pd.ExcelWriter(
        output_file
        ,date_format     = 'dd/MM/yyyy'
        ,datetime_format = 'dd/MM/yyyy HH:MM:SS'
    )
    
    # Get the XlsxWriter objects from the file descriptor.
    workbook = writer.book
    
    for sheet, df1data in df1.items():
        # Check if the worksheet name in file1 exists in file2.
        if sheet in df2:
            # Assign the worksheet content from file2 into a variable.
            df2data = df2[sheet]
            
            # Change the datetime dtype into date dtype.
            df1data['Date']       = df1data['Date'].dt.date
            
            # Change the datetime dtype into date dtype.
            df2data['Date']       = df2data['Date'].dt.date
            
            # Using Key1, filter out duplicated rows.
            df1uniq = df1data[~df1data['Key1'].isin(df2data['Key1'])]
            df2uniq = df2data[~df2data['Key1'].isin(df1data['Key1'])]
            
            # Merge the new rows from both dfs into a new df.
            df = pd.concat([df1uniq, df2uniq], ignore_index=True)
            
            # Get the dimensions of the dataframe. If empty, skip worksheet creation.
            if len(df) == 0:
                continue
            else:
                (max_row, max_col) = df.shape
            
            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(writer, sheet_name=sheet + '_new', startrow=1, header=False, index=False)
            
            # Create a list of column headers, to use in add_table().
            column_settings = [{'header': column} for column in df.columns]
            
            # Get the XlsxWriter objects from the dataframe writer object.
            ws = writer.sheets[sheet + '_new']
            
            # Add the Excel table structure. Pandas will add the data.
            ws.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
            
            # Default to zoom 85%.
            ws.set_zoom(85)
            
            # Delete dataframe.
            del df
          
    # Check for changed content.
    for sheet, df1data in df1.items():
        # Check if the worksheet name in file1 exists in file2.
        if sheet in df2:
            # Assign the worksheet content from file2 into a variable.
            df2data = df2[sheet]
            
            # Drop unique rows from df2 (assume df1 will always have lesser rows).
            df2data = df2data[df2data['Key1'].isin(df1data['Key1'])]
            
            # Construct the boolean array of both dfs.
            dfdiff = df1data.values == df2data.values
            
            # Split the boolean array into rows and cells for unmatched only.
            rows, cols = np.where(dfdiff == False)
            
            # Initialize the df.
            df = pd.DataFrame(columns=['Key1'])
            
            # Aggregate both rows and cols into a list and iterate through.
            for item in zip(rows, cols):
                # Check only if one of the cells in either df have non-NaN values.
                if not pd.isna(df1data.iloc[item[0], item[1]]) \
                    or not pd.isna(df2data.iloc[item[0], item[1]]):
                    row, col = item
                    
                    # Construct the df for the changed content.
                    new_row = pd.DataFrame({'Key1': df1data.iloc[row,0], df1data.columns[col]: '{} => {}'.format(df1data.iloc[item[0], item[1]], df2data.iloc[item[0], item[1]])}, index=[0])
                    
                    # Merge the new change into the list
                    df = df.merge(new_row, how='outer')
                    
            # Combine the rows with same Key1 into a single row.
            df = df.groupby(by='Key1').first().sort_values(by=['Key1'], key=lambda col: col.str.lower().astype(int)).reset_index().fillna('')
            
            # Get the dimensions of the dataframe. If empty, skip worksheet creation.
            if len(df) == 0:
                continue
            else:
                (max_row, max_col) = df.shape
            
            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(writer, sheet_name=sheet + '_changed', startrow=1, header=False, index=False)
            
            # Create a list of column headers, to use in add_table().
            column_settings = [{'header': column} for column in df.columns]
            
            # Get the XlsxWriter objects from the dataframe writer object.
            ws = writer.sheets[sheet + '_changed']
            
            # Add the Excel table structure. Pandas will add the data.
            ws.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
            
            # Default to zoom 85%.
            ws.set_zoom(85)
            
            # Delete dataframe.
            del df
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.close()
    
    # Print export successful.
    print('Export OK: ' + output_file)
    
except Exception as e:
    # Print error and stop program execution.
    print('Export FAILED: ' + output_file + '\r\n' + str(e))
    quit()
    
finally:
    # Garbage collect.
    gc.collect()

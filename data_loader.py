import datetime
import os
from os import listdir
from os.path import isfile, join

import xlrd

# constants
SALES_FILE_LOCATION = os.getcwd() + '\data\sales'
SALES_SHEET_NAME = 'Sales Contact Lens Credit'

SALES_COLUMN_IDX_FOR_INVOICE = 3
SALES_COLUMN_IDX_FOR_DATE = 0
SALES_COLUMN_IDX_FOR_CLIENT_NAME = 2
SALES_COLUMN_IDX_FOR_VOUCHER_NO = 4
SALES_COLUMN_IDX_FOR_PRODUCT_NAME = 0
SALES_COLUMN_IDX_FOR_PRODUCT_AMOUNT = 1
SALES_COLUMN_IDX_FOR_PRODUCT_TOTAL_PRICE = 3

DISCOUNT_FILE_LOCATION = os.getcwd() + '\data\discount'
DISCOUNT_SHEET_IDX = 0
DISCOUNT_COLUMN_IDX_FOR_DATE = 0
DISCOUNT_COLUMN_IDX_FOR_CLIENT_NAME = 2
DISCOUNT_COLUMN_IDX_FOR_VOUCHER_NO = 4
DISCOUNT_COLUMN_IDX_FOR_AMOUNT = 5

RETURN_FILE_LOCATION = os.getcwd() + '\data\\return'
RETURN_SHEET_IDX = 0
RETURN_COLUMN_IDX_FOR_DATE = 0
RETURN_COLUMN_IDX_FOR_CLIENT_NAME = 2
RETURN_COLUMN_IDX_FOR_VOUCHER_NO = 4
RETURN_COLUMN_IDX_FOR_AMOUNT = 5

# read sales data
sales_files = [f for f in listdir(SALES_FILE_LOCATION) if isfile(join(SALES_FILE_LOCATION, f))]

for sales_file in sales_files:
    file_location = SALES_FILE_LOCATION + '\\' + sales_file
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_name(SALES_SHEET_NAME)
    startRow = 0
    voucherId = -1
    clientId = -1

    while True:
        if sheet.cell_value(startRow, SALES_COLUMN_IDX_FOR_INVOICE) == 'Invoice':
            break
        startRow += 1

    for rowIdx in range(startRow, sheet.nrows):
        if sheet.cell_value(rowIdx, 0) == '':
            break
        if sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_INVOICE) == 'Invoice':
            # clientId = save_client_or_return_client_id_if_exists(
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_CLIENT_NAME))
            # provide random salesmanId and locationId
            time_tuple = xlrd.xldate_as_tuple(sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_DATE), 0)
            date = datetime.datetime(*time_tuple)
            # voucherId = save_voucher(
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_VOUCHER_NO),
            #                           clientId, date)
        else:
            # assert that clientId and voucherId >= 0
            # productId = save_product_or_return_product_id_if_exists(
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_NAME))
            # save_transaction ('PURCHASE', voucherId, productId,
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_AMOUNT)
            #                           sheet.cell_value(rowIdx, SALES_COLUMN_IDX_FOR_PRODUCT_TOTAL_PRICE))
            print()
        rowIdx += 1

# read discount data
discount_files = [f for f in listdir(DISCOUNT_FILE_LOCATION) if isfile(join(DISCOUNT_FILE_LOCATION, f))]

for discount_file in discount_files:
    file_location = DISCOUNT_FILE_LOCATION + '\\' + discount_file
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(DISCOUNT_SHEET_IDX)
    rowIdx = 0

    while True:
        if sheet.cell_type(rowIdx, DISCOUNT_COLUMN_IDX_FOR_DATE) == xlrd.XL_CELL_DATE:
            break
        rowIdx += 1

    while True:
        if sheet.cell_type(rowIdx, DISCOUNT_COLUMN_IDX_FOR_DATE) != xlrd.XL_CELL_DATE:
            break
        # clientId = save_client_or_return_client_id_if_exists(
        #                           sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_CLIENT_NAME))
        # provide random salesmanId and locationId
        time_tuple = xlrd.xldate_as_tuple(sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_DATE), 0)
        date = datetime.datetime(*time_tuple)
        # voucherId = save_voucher(
        #                           sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_VOUCHER_NO),
        #                           clientId, date)
        # save_transaction ('DISCOUNT', voucherId, null,
        #                           null,
        #                           sheet.cell_value(rowIdx, DISCOUNT_COLUMN_IDX_FOR_AMOUNT))
        rowIdx += 1

# read return data
return_files = [f for f in listdir(RETURN_FILE_LOCATION) if isfile(join(RETURN_FILE_LOCATION, f))]

for return_file in return_files:
    file_location = RETURN_FILE_LOCATION + '\\' + return_file
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(RETURN_SHEET_IDX)
    rowIdx = 0

    while True:
        if sheet.cell_type(rowIdx, RETURN_COLUMN_IDX_FOR_DATE) == xlrd.XL_CELL_DATE:
            break
        rowIdx += 1

    while True:
        if sheet.cell_type(rowIdx, RETURN_COLUMN_IDX_FOR_DATE) != xlrd.XL_CELL_DATE or rowIdx > 5:
            break
        # clientId = save_client_or_return_client_id_if_exists(
        #                           sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_CLIENT_NAME))
        # provide random salesmanId and locationId
        time_tuple = xlrd.xldate_as_tuple(sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_DATE), 0)
        date = datetime.datetime(*time_tuple)
        # voucherId = save_voucher(
        #                           sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_VOUCHER_NO),
        #                           clientId, date)
        # save_transaction ('RETURN', voucherId, null,
        #                           null,
        #                           sheet.cell_value(rowIdx, RETURN_COLUMN_IDX_FOR_AMOUNT))
        rowIdx += 1

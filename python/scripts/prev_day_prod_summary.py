#! python3

#python script to parse the server to get the no. of products shot the day before

#TO-DO
#[Done]1. ignore pre-market session for regular Ralph Lauren
#[Done] 2. exclude model sessions
#3. fill shot column on each shotlist

import json
import re
import struct
import sys
import xattr
from datetime import date, timedelta
from pathlib import Path
from time import sleep

import gspread
import pyinputplus as pyip

def main():
    #prompt the user to see if yesterday is public holiday, and amend the days to be subtracted from today
    holiday_check = pyip.inputYesNo('Is yesterday public holiday? (Y/N): ')
    day_to_subtract = 2 if holiday_check == "yes" else 1

    #prompt for custom date
    custom_date_yes_no = pyip.inputYesNo('Do you want to check a custom date? (Y/N): ')
    if custom_date_yes_no == 'yes':
        custom_year = date.today().year
        custom_month = pyip.inputNum('Month (1-12): ')
        custom_day = pyip.inputNum('Day (1-31): ')
        check_date = date(custom_year, custom_month, custom_day)
    else:
        #construct check_date as yesterday or last friday if today is Monday
        check_date = date.today() - timedelta(days=3) if date.today().strftime('%a') == 'Mon' else date.today() - timedelta(days=day_to_subtract)

    print(f'\nChecking production for {check_date}')
    print('Parsing server...')

    brand_data = {
            'Agnes b': {'folder': 'Agnes B/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([A-Z0-9]+_[0-9]{3,4})_([0-9])(|_COMP[0-9]+|_INSERT)\\.tif'},
            'AIWA': {'folder': 'AIWA EUROPE/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([-A-Z0-9]+)_([\\sA-Z0-9]+)(|_COMP[0-9]{1,2})\\.tif'},
            'Alphabox': {'folder': 'Alphabox/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': ''},
            'Arena': {'folder': 'Arena/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([A-Z0-9]+)(_[0-9])(|_TOP|_BOTTOM)(|_COMP[0-9]?|_INSERT)(|_[a-zA-Z0-9\\s]+)\\.tif'},
            'Chevignon': {'folder': 'Chevignon/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([A-Z0-9]+)(_[1-9])(|_COMP[0-9]?|_INSERT)(|_[a-zA-Z0-9\\s]+)\\.tif'},
            'Fred Perry': {'folder': 'Fred Perry/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([A-Z0-9]{2,7}_[A-Z0-9]{3})_V2_Q[\\d]{3}_([A-Z0-9]+)(|_COMP[0-9]?[ a-zA-Z0-9]*|_Comp[0-9]?[ a-zA-Z0-9]*|_INSERT)\\.tif'},
            'Lojel': {'folder': 'Lojel/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([^_]+)(|_.+)\\.tif'},
            'Kipling': {'folder': 'Kipling/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '(KPK[A-Z0-9]+)_(\\d|DSO)\\.tif'},
            'New Balance': {'folder': 'New Balance/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': ''},
            'OnTheList': {'folder': 'On the List/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([a-zA-Z0-9-]+)(_[1-9]|-[1-9])(|_COMP[0-9]+|_INSERT)\\.tif'},
            'Petit Bateau': {'folder': 'Petit Bateau/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([A-Z0-9]+)_([A-Z0-9]+|[0-9]+)\\.tif'},
            'Satami': {'folder': 'Satami/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': "([A-Z]{2}-[A-Z0-9]+-[A-Z0-9]{2})_(FRONT|BACK|DETAIL)(|_COMP[0-9]+|_INSERT)\\.tif"},
            'Sau Lee': {'folder': 'Sau Lee/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': ''},
            'Speedo': {'folder': 'Arena/Production/', 'session': check_date.strftime('%Y%m%d') + '_Speedo' + '*', 'prod_re': '([A-Z0-9]+)(_[0-9])(|_TOP|_BOTTOM)(|_COMP[0-9]+|_INSERT)(|_[a-zA-Z0-9\\s]+)\\.tif'},
            'Tommy Hilfiger': {'folder': 'Tommy Hilfiger/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([A-Z0-9]+)[^tif]+\\.tif'},
            'Toys R Us': {'folder': 'Toys R Us/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': ''},
            'Ralph Lauren': {'folder': 'Ralph Lauren/Production/', 'session': check_date.strftime('%m%d%Y') + '*[!T]', 'prod_re': '([0-9]+)_([-a-zA-Z0-9]+)(|_[a-zA-Z0-9]+)\\.tif'},
            'Ralph Lauren Premarket': {'folder': 'Ralph Lauren/Production/', 'session': check_date.strftime('%m%d%Y') + '*PREMARKET*', 'prod_re': '([0-9]+)_([-a-zA-Z0-9]+)(|_[a-zA-Z0-9]+)\\.tif'},
            'Vans': {'folder': 'Vans/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([0-9]+)_([-a-zA-Z]+)(|_[a-zA-Z0-9]+)\\.tif'},
            'WEAT': {'folder': 'WEAT/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([^_]+)(|_[^\\.]+)\\.tif'}
            }

    service_account_json = Path('/Users/zeric.chan/.zeric/resources/service_account.json')
    with service_account_json.open(mode='r', encoding='utf-8') as cred_json:
        #convert to dict type as gspread.auth.service_account accepts only filename path or dict
        cred_dict = json.load(cred_json)
    gc = gspread.service_account_from_dict(cred_dict)
    ppbook = gc.open('2023 HK Production Planning')
    status_sheet = ppbook.worksheet('Brand Status')

    #Brand Status sheet
    statsheet_status_col = status_sheet.find('Status').col
    statsheet_brand_col = status_sheet.find('Brand').col
    active_brand_cells = status_sheet.findall('Active', in_column=statsheet_status_col)
    active_brand_List = []
    for active_cell in active_brand_cells:
        brand = status_sheet.cell(active_cell.row, statsheet_brand_col).value
        #check if brand data exists
        if not brand in brand_data.keys():
            sys.exit(f'Error: {brand} data is missing')
        active_brand_List.append(brand)

    #Brand Summary sheet
    summary_sheet = ppbook.worksheet('Production Summary')
    prod_shot_ytd_col = summary_sheet.find('Products Shot Ytd').col
    prod_need_reshoot_col = summary_sheet.find('Products need Reshoot').col
    total_row = summary_sheet.find('Total').row
    total_shot_ytd_cell = summary_sheet.cell(total_row, prod_shot_ytd_col).address
    total_need_reshoot_cell = summary_sheet.cell(total_row, prod_need_reshoot_col).address

    grand_product_shot = 0
    grand_product_need_reshoot = 0

    server_path = Path("/Volumes/Studio/CLIENTS/")
    while not server_path.is_dir():
        print('Server is not connected')
        sleep(10)

    for brand in brand_data.keys():
        if brand in active_brand_List:
            print('\n==========================================================================================\n')
            print(f'\nAccessing {brand} production data...\n')
            brand_prod_path = server_path / brand_data[brand]['folder']
            session_shot_yesterday_list = brand_prod_path.glob(brand_data[brand]['session'])
            product_list = [] #products been shot
            reshot_product_list = [] #products been reshot
            reshoot_product_list = [] #products need reshoot
            brand_img_name = re.compile(r'{}'.format(brand_data[brand]['prod_re']))
            print('Brand: ' + brand + '\n')

            for session in session_shot_yesterday_list:
                if 'model' in session.name.lower() or 'creative' in session.name.lower():
                    continue
                print(session.name)
                img_list = sorted((session / 'Output').glob('**/*.tif'))
                for img in img_list:
                    try :
                        product = brand_img_name.fullmatch(img.name).group(1)
                    except AttributeError:
                        print(f'\nThe image {img.name} does not match with the Regex')
                        ans = ''
                        while ans == '':
                            ans = input('ignore? (Y/N): ')
                            if ans.lower() == 'y' or ans.lower() == 'yes':
                                product = ''
                                while product == '':
                                    product = input('Please manually input the product code: ')
                                break
                            elif ans.lower() == 'n' or ans.lower() == 'no':
                                sys.exit(2)
                            else:
                                ans = ''
                                continue

                    #parse the img metadata to check if it is mac colour-labelled
                    colour_label = struct.unpack("<16H", xattr.getxattr(img, "com.apple.FinderInfo"))
                    if colour_label[4] != 0 and colour_label[4] != 2048:
                        # if colour_label[4] == 3072:
                            # print(f'{img.name} --- red label')
                        # elif colour_label[4] == 3584:
                            # print(f'{img.name} --- orange label')

                        if product not in reshoot_product_list:
                            reshoot_product_list.append(product)
                        if product in reshot_product_list:
                            reshot_product_list.remove(product)
                        if product in product_list:
                            product_list.remove(product)
                        continue

                    if 'reshoot' in str(img.absolute()).lower() or 'reshot' in str(img.absolute()).lower():
                        if product not in reshot_product_list:
                            reshot_product_list.append(product)
                        continue

                    if product not in product_list:
                        product_list.append(product)
                    
            num_product_shot_ytd = len(product_list)
            num_product_need_reshoot = len(reshoot_product_list)
            num_product_reshot_ytd = len(reshot_product_list)
            grand_product_shot += num_product_shot_ytd
            grand_product_need_reshoot += num_product_need_reshoot

            #Write to Production Summary brand row
            try:
                brand_row = summary_sheet.find(brand).row
            except AttributeError:
                print(f'Error: {brand} cannot be found on "Brand Summary" worksheet.')
                continue
            prod_shot_ytd_cell = summary_sheet.cell(brand_row, prod_shot_ytd_col).address
            prod_need_reshoot_cell = summary_sheet.cell(brand_row, prod_need_reshoot_col).address
            summary_sheet.update(prod_shot_ytd_cell, num_product_shot_ytd) if num_product_shot_ytd != 0 else print(f'--- No products shot for {brand} ---')
            summary_sheet.update(prod_need_reshoot_cell, num_product_need_reshoot) if num_product_need_reshoot != 0 else print(f'--- No products need reshoot for {brand} ---')

            #Terminal Reporting
            if product_list != []:
                print(f'\nNo. of products shot: {num_product_shot_ytd}')

            if reshot_product_list != []:
                print(f'No. of products reshot: {num_product_reshot_ytd}')

            if reshoot_product_list != []:
                print(f'No. of products need reshoot: {num_product_need_reshoot}')
                print('\nProducts Required Reshoot:')
                for prod in reshoot_product_list:
                    print("\t" + prod)

    #Write to Production Summary Total row
    summary_sheet.update(total_shot_ytd_cell, grand_product_shot)
    summary_sheet.update(total_need_reshoot_cell, grand_product_need_reshoot)
    print('\n==========================================================================================\n')

if __name__ == "__main__":
    main()

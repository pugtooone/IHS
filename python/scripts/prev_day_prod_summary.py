#! python3

#python script to parse the server to get the no. of products shot the day before

#TO-DO
#[Done]1. ignore pre-market session for regular Ralph Lauren
#[Done] 2. exclude model sessions
#3. fill shot column on each shotlist
#4. test print(*list)

import json
import re
import struct
import sys
import xattr
from datetime import date, timedelta
from pathlib import Path
from time import sleep

import gspread

#construct check_date as yesterday or last friday if today is Monday
check_date = date.today() - timedelta(days=3) if date.today().strftime('%a') == 'Mon' else date.today() - timedelta(days=1)

brand_data = {
        'Agnes b': {'folder': 'Agnes B/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([A-Z0-9]+_[0-9]{3,4})_([0-9])(|_COMP[0-9]+|_INSERT)\\.tif'},
        'Alphabox': {'folder': 'Alphabox/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': ''},
        'Arena': {'folder': 'Arena/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([A-Z0-9]+)(_[0-9])(|_TOP|_BOTTOM)(|_COMP[0-9]?|_INSERT)(|_[a-zA-Z0-9\\s]+)\\.tif'},
        'Fred Perry': {'folder': 'Fred Perry/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([A-Z0-9]{2,7}_[A-Z0-9]{3})_V2_Q124_([A-Z0-9]+)(|_COMP[0-9]?[ a-zA-Z0-9]*|_INSERT)\\.tif'},
        'Kipling': {'folder': 'Kipling/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '(KPK[A-Z0-9]+)_(\\d|DSO)\\.tif'},
        'New Balance': {'folder': 'New Balance/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': ''},
        'OnTheList': {'folder': 'On the List/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([a-zA-Z0-9-]+)(_1|_2|-[1-9])(|_COMP[0-9]+|_INSERT)\\.tif'},
        'Sau Lee': {'folder': 'Sau Lee/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': ''},
        'Speedo': {'folder': 'Arena/Production/', 'session': check_date.strftime('%Y%m%d') + '_Speedo' + '*', 'prod_re': '([A-Z0-9]+)(_[0-9])(|_TOP|_BOTTOM)(|_COMP[0-9]+|_INSERT)(|_[a-zA-Z0-9\\s]+)\\.tif'},
        'Tommy Hilfiger': {'folder': 'Tommy Hilfiger/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': 'C11_02_AAA([A-Z0-9]+)_(FL|MO)-ST-([BDF][1-2])\\.tif'},
        'Toys R Us': {'folder': 'Toys R Us/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': ''},
        'Ralph Lauren': {'folder': 'Ralph Lauren/Production/', 'session': check_date.strftime('%m%d%Y') + '*[!T]', 'prod_re': '([0-9]+)_([-a-zA-Z0-9]+)(|_[a-zA-Z0-9]+)\\.tif'},
        'Ralph Lauren Premarket': {'folder': 'Ralph Lauren/Production/', 'session': check_date.strftime('%m%d%Y') + '*PREMARKET*', 'prod_re': '([0-9]+)_([-a-zA-Z0-9]+)(|_[a-zA-Z0-9]+)\\.tif'},
        'Vans': {'folder': 'Vans/Production/', 'session': check_date.strftime('%Y%m%d') + '*', 'prod_re': '([0-9]+)_([-a-zA-Z]+)(|_[a-zA-Z0-9]+)\\.tif'}
        }

def main():
    service_account_json = Path('/Users/zeric.chan/.zeric/resources/service_account.json')
    with service_account_json.open(mode='r', encoding='utf-8') as cred_json:
        #convert to dict type as gspread.auth.service_account accepts only filename path or dict
        cred_dict = json.load(cred_json)
    gc = gspread.service_account_from_dict(cred_dict)
    ppbook = gc.open('2023 HK Production Planning')
    status_sheet = ppbook.worksheet('Brand Status')
    # ssbook = gc.open('IHS Studio Schedule 2023')
    # schedule_sheet = ssbook.worksheet('Studio Schedule')

    #Brand Status sheet
    statsheet_status_col = status_sheet.find('Status').col
    statsheet_brand_col = status_sheet.find('Brand').col
    active_brand_cells = status_sheet.findall('Active', in_column=statsheet_status_col)
    active_brand_List = []
    for active_cell in active_brand_cells:
        brand = status_sheet.cell(active_cell.row, statsheet_brand_col).value
        active_brand_List.append(brand)

    #Brand Summary sheet
    summary_sheet = ppbook.worksheet('Brand Summary')
    to_write_col = summary_sheet.find('Products Shot Ytd').col
    total_row = summary_sheet.find('Total').row
    total_cell = summary_sheet.cell(total_row, to_write_col).address

    #Studio Schedule sheet
    # schsheet_brand_col = schedule_sheet.find('Brand').col
    # schsheet_date_format = yesterday.strftime('%a, %d %m')

    grand_product_shot = 0;

    server_path = Path("/Volumes/Studio/CLIENTS/")
    while not server_path.is_dir():
        print('Server is not connected')
        sleep(10)

    for brand in brand_data.keys():
        if brand in active_brand_List:
            brand_prod_path = server_path / brand_data[brand]['folder']
            session_shot_yesterday_list = brand_prod_path.glob(brand_data[brand]['session'])
            product_list = [] #products been shot
            reshot_produuct_list = [] #products been reshot
            reshoot_product_list = [] #products need reshoot
            brand_img_name = re.compile(r'{}'.format(brand_data[brand]['prod_re']))
            print('\n==========================================================================================\n')
            print('Brand: ' + brand + '\n')

            for session in session_shot_yesterday_list:
                if 'model' in session.name.lower():
                    continue
                print(session.name)
                img_list = sorted((session / 'Output').glob('**/*.tif'))
                for img in img_list:
                    try :
                        product = brand_img_name.fullmatch(img.name).group(1)
                    except AttributeError:
                        print(f'The image {img.name} does not match with the Regex')
                        ans = ''
                        while ans == '':
                            ans = input('\nignore? (Y/N): ')
                            if ans.lower() == 'y':
                                product = input('Please manually input the product code: ')
                                break
                            elif ans.lower() == 'n':
                                sys.exit(1)

                    #parse the img metadata to check if it is mac colour-labelled
                    colour_label = struct.unpack("<16H", xattr.getxattr(img, "com.apple.FinderInfo"))
                    if colour_label[4] != 0 and colour_label[4] != 2048:
                        # if colour_label[4] == 3072:
                            # print(f'{img.name} --- red label')
                        # elif colour_label[4] == 3584:
                            # print(f'{img.name} --- orange label')

                        if product not in reshoot_product_list:
                            reshoot_product_list.append(product)
                        if product in reshot_produuct_list:
                            reshot_produuct_list.remove(product)
                        if product in product_list:
                            product_list.remove(product)
                        continue

                    if img.parent.name.lower() == "reshoot" or img.parent.name.lower() == "reshot":
                        reshot_produuct_list.append(product)
                        continue

                    if product not in product_list:
                        product_list.append(product)
                    
            num_product_shot_ytd = len(product_list)
            grand_product_shot += num_product_shot_ytd

            summary_sheet = ppbook.worksheet('Brand Summary')
            to_write_col = summary_sheet.find('Products Shot Ytd').col
            try:
                to_write_row = summary_sheet.find(brand).row
            except AttributeError:
                print(f'Error: {brand} cannot be found on "Brand Summary" worksheet.')
                continue
            cell_to_write = summary_sheet.cell(to_write_row, to_write_col).address
            summary_sheet.update(cell_to_write, num_product_shot_ytd)

            #Terminal Reporting
            if product_list != []:
                print(f'\nNo. of products shot: {num_product_shot_ytd}')

            num_product_reshot_ytd = len(reshot_produuct_list)
            if reshot_produuct_list != []:
                print(f'No. of products reshot: {num_product_reshot_ytd}')

            if reshoot_product_list != []:
                print('\nProducts Required Reshoot:')
                print(*reshoot_product_list)

    summary_sheet.update(total_cell, grand_product_shot)
    print('\n==========================================================================================\n')

if __name__ == "__main__":
    main()

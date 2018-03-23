import datetime
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from google_drive_api_files_wrapper import File


# for seq, item in enumerate(items):
#     filename, file_extension = os.path.splitext(item['name'])
#     file_extension = file_extension[1:]  # File Extension Name
#     filename_item = filename.split('_')  # File Name Split Array
#
#     # Define each component from the file name into a dict (key, value)
#     item_dict = {'Date': datetime.datetime.strptime(str(filename_item[0]), "%Y%m%d").date(),
#                  'Currency': filename_item[1],
#                  'Paid': float(filename_item[2]),
#                  'Supplier_EN': split_by_parenthesis(str(filename_item[3]))[0],
#                  'Supplier_LOCAL': split_by_parenthesis(str(filename_item[3]))[1],
#                  'Format': file_extension,
#                  'ID': item['id'],
#                  'ParentID': item['parents']
#                  }
#     google_data.append(item_dict)
# # Define the Header
# google_data_header = ['Format', 'Date', 'Paid', 'Currency', 'Supplier_EN', 'Supplier_LOCAL']
# # Dictionary return
# google_data_return = {
#     'header': google_data_header,
#     'data': google_data
# }


def split_by_parenthesis(string):
    left, right = string.find('('), string.find(')')
    if not(left == right == -1):
        string = [string[:left], string[left+1:right]]
    else:
        string = [string, string]
    return string


def main():
    google_file = File()
    # Refer to Google Drive API : https://developers.google.com/drive/v3/reference/files/list
    file_list_kwargs = {
        'spaces': 'drive',
        'orderBy': 'name',  # 'createdTime', 'folder', 'modifiedByMeTime', 'modifiedTime', 'name', 'name_natural', 'quotaBytesUsed', 'recency', 'sharedWithMeTime', 'starred', and 'viewedByMeTime'
        'pageSize': 1000,
        'fields': "nextPageToken, files(id, name, parents)",
        'q': """
            trashed != true
            and mimeType != 'application/vnd.google-apps.folder'
            """
    }
    df = pd.DataFrame(google_file.list(**file_list_kwargs))
    df.columns = ['id', 'name', 'parent_id']
    print(df.head())

    # df = pd.DataFrame(data=data_dict['data'], columns=data_dict['header'])
    # min_date, max_date = df['Date'].min(), df['Date'].max()
    # # print(df)
    #
    # """ Save output
    # """
    # output_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'out.csv')
    # df.to_csv(output_dir, encoding='utf-8-sig')
    #
    # """ Prepare Plotting Data
    # """
    # df_by_date = df.groupby('Date')['Paid'].agg(['count', 'sum', 'min', 'max', 'mean'])
    # df_by_date.columns = ['Invoices', 'TotalPaid', 'MinPaid', 'MaxPaid', 'MeanPaid']
    # print(df_by_date)
    #
    # df_by_supplier = df.groupby('Supplier_LOCAL')['Paid'].agg(['count', 'sum', 'min', 'max', 'mean'])
    # df_by_supplier.columns = ['Invoices', 'TotalPaid', 'MinPaid', 'MaxPaid', 'MeanPaid']
    # print(df_by_supplier)
    #
    # """ Plotting : Globals
    # """
    # mpl.rcParams['font.sans-serif'] = ['SimHei']  # Showing Chinese Characters
    # mpl.rcParams['font.serif'] = ['SimHei']  # Showing Chinese Characters
    #
    # fig = plt.figure()
    # grid = mpl.gridspec.GridSpec(nrows=2, ncols=2, width_ratios=[5, 6], height_ratios=[2, 1])
    # ax1 = fig.add_subplot(grid[0, 0])
    # ax2 = fig.add_subplot(grid[1, 0])
    # ax3 = fig.add_subplot(grid[:, 1])
    # fig.tight_layout()
    # fig.canvas.set_window_title('Expenditure summarized by receipts & invoices collected in Google Drive')
    #
    # """ Plotting : Axes
    # """
    # series1 = df_by_date['TotalPaid']
    # series2 = pd.Series(index=series1.index, data=series1.values.mean())
    # ax1.plot(series1.index, series1.values, 'b-o', series2.index, series2.values, 'r-')
    # ax1.set(xlabel='Date', ylabel='Invoice Paid', title='General Expenditure By Date({})'.format(len(series1.index)))
    # ax1.grid()
    #
    # series1 = df_by_date['Invoices']
    # series2 = pd.Series(index=series1.index, data=series1.values.mean())
    # ax2.plot(series1.index, series1.values, 'g-*', series2.index, series2.values, 'r-')
    # ax2.set(xlabel='Date', ylabel='Number Collected', title='No. Invoices/Receipts By Date({})'.format(len(series1.index)))
    # ax2.grid()
    #
    # series1 = df_by_supplier['TotalPaid']
    # ax3.pie(series1.values, labels=series1.index, autopct='%1.1f%%', shadow=False, startangle=90)
    # ax3.set(title='General Expenditure By Supplier ({}), from {} to {}'.format(len(series1.index), min_date, max_date))
    #
    # """ Plotting : Plot & Show
    # """
    # plt.style.use('ggplot')
    # plt.show()


if __name__ == '__main__':
    main()

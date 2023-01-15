import pandas as pd
import numpy as np
import sys


def main():
    args = sys.argv

    # 監視対象の
    num_watchlist = 4
    # 監視ファイルの読み込み
    # "-"が含まれているためresponse_msecはstringで読み込む
    dtype_log = {'datetime': 'string',
                 'ip': 'category', 'response_msec': 'string'}
    df = pd.read_csv('./log/samplelog.csv', dtype=dtype_log)

    np_report = np.empty((0, 3), dtype='object')
    for idx_ip in range(num_watchlist):
        ip_name = df.iat[idx_ip, 1]
        df_thisip = df.loc[idx_ip::num_watchlist]
        # '-'のときに1、実時間応答があるときは0とする
        np_index = np.where(
            df_thisip['response_msec'] == '-', 1, 0).astype('int8')
        np_index_diff = np_index[1:] - np_index[:-1]
        # 設問1：タイムアウトの始まりと終わりを探す
        np_index_start_timeout = np.where(np_index_diff == 1)[0] + 1
        np_index_end_timeout = np.where(np_index_diff == -1)[0] + 1

        for i in range(np_index_end_timeout.size):
            df_index_start_timeout = np_index_start_timeout[i]
            df_index_end_timeout = np_index_end_timeout[i]
            np_report = np.append(np_report, np.array([[ip_name, df_thisip.iat[df_index_start_timeout,
                                                                               0], df_thisip.iat[df_index_end_timeout, 0]]]), axis=0)
            print(ip_name + ',' + df_thisip.iat[df_index_start_timeout,
                  0]+','+df_thisip.iat[df_index_end_timeout, 0])

    columns_report = ['ip', 'datetime_start_timeout', 'datetime_end_timeout']
    df_report = pd.DataFrame(data=np_report, columns=columns_report)
    df_report.to_csv('./report/report1_.csv', index=False)


if __name__ == '__main__':
    main()

import pandas as pd
import numpy as np
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True,
                        help='読み込む監視ログファイルのパス')
    parser.add_argument('-N', '--numoftimeout',
                        required=True, help='故障とみなす連続タイムアウト回数  設問2用')
    parser.add_argument('-d', '--dst', required=False,
                        help='レポートの出力先のパス 指定しない場合は規定のフォルダ下に出力する')


def main():
    args = get_args()
    file = './log/samplelog.csv'  # args.file
    N = 2  # args.numoftimeout
    name_report = './report/report1_.csv'  # +args.dst

    # 監視対象の
    num_watchlist = 4
    # 監視ファイルの読み込み
    # "-"が含まれているためresponse_msecはstringで読み込む
    dtype_log = {'datetime': 'string',
                 'ip': 'category', 'response_msec': 'string'}
    df = pd.read_csv(file, dtype=dtype_log)

    np_report = np.empty((0, 3), dtype='object')
    for idx_ip in range(num_watchlist):
        ip_name = df.iat[idx_ip, 1]
        df_thisip = df.loc[idx_ip::num_watchlist]

        # 設問1：タイムアウトの始まりと終わりを検出する
        # '-'のときに1、実時間応答があるときは0とする
        np_index = np.where(
            df_thisip['response_msec'] == '-', 1, 0).astype('int16')
        np_index_diff = np_index[1:] - np_index[:-1]
        np_index_start_timeout = np.where(np_index_diff == 1)[0] + 1
        np_index_end_timeout = np.where(np_index_diff == -1)[0] + 1
        # 監視ログファイル最後の記録がタイムアウトである(ファイル内で終了が検出出来ない)場合の判定

        if np_index_end_timeout.size != np_index_start_timeout.size:
            np_index_end_timeout = np.append(
                [np_index.size-1], np_index_end_timeout)
        num_timeout = np_index_start_timeout.size

        for i in range(num_timeout):
            datetime_start_timeout = df_thisip.iat[np_index_start_timeout[i], 0]
            datetime_end_timeout = df_thisip.iat[np_index_end_timeout[i], 0]
            np_report = np.append(np_report, np.array(
                [[ip_name, datetime_start_timeout, datetime_end_timeout]]), axis=0)
            print(ip_name + ',' + datetime_start_timeout +
                  ','+datetime_end_timeout)

    columns_report = ['ip', 'datetime_start_timeout', 'datetime_end_timeout']
    df_report = pd.DataFrame(data=np_report, columns=columns_report)
    df_report.to_csv(name_report, index=False)


if __name__ == '__main__':
    main()

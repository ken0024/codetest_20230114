
import numpy as np
import pandas as pd
import argparse
import random
import os

PATH_WATCHLIST = os.getcwd()+'/log/watchlist.txt'
RESPONSE_TIMEOUT = 1000


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', required=True, type=str,
                        help='生成する監視ログの初期時間(%Y-%m-%dT%H:%M:%S)')
    parser.add_argument('-n', '--num', required=True, type=int,
                        help='生成する監視ログのipごとの記録数')
    parser.add_argument('-i', '--interval', required=True, type=int,
                        help='生成する監視ログのping応答の時間間隔(sec)')
    return parser.parse_args()


def main():
    args = get_args()
    date_init = np.datetime64(args.date)
    duration_pingtest = args.interval

    num_records = args.num
    watchlist = np.loadtxt(PATH_WATCHLIST, dtype='object').tolist()
    num_watchlist = len(watchlist)

    list_ping = [random.randint(20, 100) for k in range(num_watchlist)]
    list_watchlist = watchlist
    tmp_datetime = [
        date_init + np.timedelta64(random.randint(0, 59), 's')for i in range(num_watchlist)]
    list_datetime = tmp_datetime

    date_end = date_init + \
        np.timedelta64(duration_pingtest*(num_records-1)+60, 's')
    # +         pd.to_datetime(date_end).strftime('%Y-%m-%dT%H:%M:%S')+'.csv'
    file_log = os.getcwd()+'/log/' + pd.to_datetime(date_init).strftime('%Y%m%d%H%M%S')+'_' +\
        pd.to_datetime(date_end).strftime('%Y%m%d%H%M%S')+'.csv'
    for j in range(num_records-1):
        # ping値の更新
        # 重みづけでping応答時間がスムーズに増減出来る様にしたい(改善点)
        list_ping = list_ping + \
            [random.randint(10, 1000) for k in range(num_watchlist)]
        # logに追加
        list_watchlist = list_watchlist + watchlist
        # タイムスタンプの更新
        tmp_datetime = tmp_datetime + np.timedelta64(duration_pingtest, 's')
        list_datetime.extend(tmp_datetime)

    # タイムアウト'-'を含む応答時間のリストに変換
    list_ping_str = [str(ping) if ping <
                     RESPONSE_TIMEOUT else '-' for ping in list_ping]
    df_watchlist = pd.DataFrame(data=list_watchlist, columns=['ip'])
    index_datetime = pd.to_datetime(list_datetime).strftime('%Y%m%d%H%M%S')
    df_datetime = pd.DataFrame(
        data=index_datetime.tolist(), columns=['datetime'])
    df_ping = pd.DataFrame(data=list_ping_str, columns=['response_msec'])
    df_log = pd.concat([df_datetime, df_watchlist, df_ping],
                       axis=1)

    df_log.to_csv(file_log, index=False)
    print('Output: '+file_log)
    return


if __name__ == '__main__':
    main()

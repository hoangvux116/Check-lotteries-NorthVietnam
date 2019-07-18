import requests
from bs4 import BeautifulSoup as bs
import argparse
id_xo_so = {'Đặc biệt': ['rs_0_0'],
            'Giải nhất': ['rs_1_0'],
            'Giải nhì': ['rs_2_{}'.format(i) for i in range(2)],
            'Giải ba': ['rs_3_{}'.format(i) for i in range(6)],
            'Giải bốn': ['rs_4_{}'.format(i) for i in range(4)],
            'Giải năm': ['rs_5_{}'.format(i) for i in range(6)],
            'Giải sáu': ['rs_6_{}'.format(i) for i in range(3)],
            'Giải bảy': ['rs_7_{}'.format(i) for i in range(4)]}


def crawl_prizes():
    ses = requests.Session()
    resp = ses.get('http://ketqua.net')
    tree = bs(resp.text, features="html.parser")
    date = tree.find(attrs={'id': 'result_date'}).text
    prize = {}
    for name, id_name in id_xo_so.items():
        if isinstance(id_name, list):
            prize[name] = [tree.find(attrs={'id': i}).text for i in id_name]
        else:
            prize[name] = [tree.find(attrs={'id': id_name}).text]
    return prize, date


def check_lo_to(nums):
    lottery, date = crawl_prizes()
    aux_lo_to, lst_lo_to = [], []
    for name, kqua in lottery.items():
        if isinstance(kqua, type([])):
            aux = [i[-2:] for i in kqua]
        else:
            aux = [kqua[-2:]]
        aux_lo_to.append(aux)
    for i in aux_lo_to:
        lst_lo_to.extend(i)
    for num in nums:
        if num in lst_lo_to:
            cnt = lst_lo_to.count(num)
            print('Chúc mừng, '
                  'bạn đã trúng {1} nháy '
                  'với Lucky Number: {0}'.format(num, cnt))
        else:
            print('{} không trùng kết quả, '
                  'Chúc bạn may mắn lần sau!!!'.format(num))
    print('-' * 66)
    print('Kết quả sổ xố hôm nay: ' + date)
    for ket_qua in lottery:
        print(ket_qua, ':', lottery[ket_qua])


def main():
    parser = argparse.ArgumentParser(
        description='Bạn có phải là người may mắn hôm nay?')
    parser.add_argument('nums', nargs='*', type=str)
    args = parser.parse_args()
    check_lo_to(args.nums)


if __name__ == "__main__":
    main()

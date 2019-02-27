from jrdb.templates.template import Template


class OW(Template):
    """
    http://www.jrdb.com/program/Oz/Owdata_doc.txt
    """
    name = 'ワイド基準オッズデータ（OW）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['year', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', '16進数(数字 or 小文字アルファベット)'],
        ['race', 'Ｒ', None, '2', '99', '7', None],
        ['contender_count', '登録頭数', None, '2', 'Z9', '9', None],
        ['duet_odds', 'ワイドオッズ', '153', '5', 'ZZ9.9', '11', 'オッズ範囲の下側を出力 5*153=765BYTE'],
        ['reserved', '予備', None, '23', 'X', '248', 'スペース'],
        ['newline', '改行', None, '2', 'X', '851', 'ＣＲ・ＬＦ'],
    ]

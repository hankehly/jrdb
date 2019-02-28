from jrdb.templates.template import Template


class OU(Template):
    """
    http://www.jrdb.com/program/Ou/Oudata_doc.txt
    """
    name = '馬単基準オッズデータ（OU）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['year', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', '16進数(数字 or 小文字アルファベット)'],
        ['race', 'Ｒ', None, '2', '99', '7', None],
        ['contender_count', '登録頭数', None, '2', 'Z9', '9', None],
        ['exacta_odds', '馬単オッズ', '306', '6', 'ZZZ9.9', '11',
         '1-2 ～ 1-18, 2-1 ～ 2-18の順 最後は、17-18。6*306=1836BYTE 取消時は 9999.9'],
        ['reserved', '予備', None, '23', 'X', '248', 'スペース'],
        ['newline', '改行', None, '2', 'X', '851', 'ＣＲ・ＬＦ'],
    ]

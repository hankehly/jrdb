from jrdb.templates.template import Template


class OT(Template):
    """
    http://www.jrdb.com/program/Ot/Otdata_doc.txt
    """
    name = '３連複基準オッズデータ（OT）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['year', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', '16進数(数字 or 小文字アルファベット)'],
        ['race', 'Ｒ', None, '2', '99', '7', None],
        ['contender_count', '登録頭数', None, '2', 'Z9', '9', None],
        ['trio_odds', '３連複オッズ', '816', '6', 'ZZZ9.9', '11', '01-02-03 ～ 最後16-17-18\n6*816=4896BYTE\n取消時は 9999.9'],
        ['reserved', '予備', None, '23', 'X', '248', 'スペース'],
        ['newline', '改行', None, '2', 'X', '851', 'ＣＲ・ＬＦ'],
    ]

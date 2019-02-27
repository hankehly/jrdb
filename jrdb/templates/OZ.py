from jrdb.templates.template import Template


class OZ(Template):
    """
    http://www.jrdb.com/program/Oz/Ozdata_doc.txt
    http://www.jrdb.com/program/Oz/Ozsiyo_doc.txt
    """
    name = 'JRDB基準オッズデータ（OZ）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['year', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', '16進数(数字 or 小文字アルファベット)'],
        ['race', 'Ｒ', None, '2', '99', '7', None],
        ['contender_count', '登録頭数', None, '2', 'Z9', '9', None],
        ['win_odds', '単勝オッズ', '18', '5', 'ZZ9.9', '11', '5*18=90BYTE'],
        ['show_odds', '複勝オッズ', '18', '5', 'ZZ9.9', '101', '5*18=90BYTE'],
        ['quinella_odds', '連勝オッズ', '153', '5', 'ZZ9.9', '191', '5*153=765BYTE'],
        ['newline', '改行', None, '2', 'X', '851', 'ＣＲ・ＬＦ'],
    ]

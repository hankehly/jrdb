from jrdb.datadocs.doctype import DocType


class SRB(DocType):
    """
    http://www.jrdb.com/program/Srb/srb_doc.txt
    """
    name = 'JRDB成績レースデータ（SRB）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['year', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', None],
        ['race', 'Ｒ', None, '2', '99', '7', None],
        ['furlong_time', 'ハロンタイム', '18', '3', '999', '9', '3*18=54BYTE 先頭馬の１ハロン毎のタイム 0.1秒単位　※１'],
        ['corner_1_pos', '１コーナー', None, '64', 'X', '63', None],
        ['corner_2_pos', '２コーナー', None, '64', 'X', '127', None],
        ['corner_3_pos', '３コーナー', None, '64', 'X', '191', None],
        ['corner_4_pos', '４コーナー', None, '64', 'X', '255', None],
        ['pace_up_pos', 'ペースアップ位置', None, '2', '9', '319', '残りハロン数'],  # 意味不明
        ['track_bias_1_corner', 'トラックバイアス（１角）', None, '3', 'X', '321', '（内、中、外）'],
        ['track_bias_2_corner', 'トラックバイアス（２角）', None, '3', 'X', '324', '（内、中、外）'],
        ['track_bias_backstretch', 'トラックバイアス（向正）', None, '3', 'X', '327', '（内、中、外）'],
        ['track_bias_3_corner', 'トラックバイアス（３角）', None, '3', 'X', '330', '（内、中、外）'],
        ['track_bias_4_corner', 'トラックバイアス（４角）', None, '3', 'X', '333', '（最内、内、中、外、大外）'],
        ['track_bias_homestretch', 'トラックバイアス（直線）', None, '3', 'X', '338', '（最内、内、中、外、大外）'],
        ['race_comment', 'レースコメント', None, '500', 'X', '343', None],
        ['reserved', '予備', None, '8', 'X', '843', 'スペース'],
        ['newline', '改行', None, '2', 'X', '851', 'ＣＲ・ＬＦ'],
    ]

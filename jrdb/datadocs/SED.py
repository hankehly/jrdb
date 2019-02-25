from jrdb.datadocs.doctype import DocType


class SED(DocType):
    name = 'JRDB成績データ（SED）'
    items = [
        ['racetrack', '場コード', None, '2', '99', '1', None],
        ['year', '年', None, '2', '99', '3', None],
        ['', '回', None, '1', '9', '5', None],
        ['number_day', '日', None, '1', 'F', '6', None],
        ['race_number', 'Ｒ', None, '2', '99', '7', None],
        ['horse_number', '馬番', None, '2', '99', '9', None],
        ['pedigree_registration_number', '血統登録番号', None, '8', 'X', '11', None],
        ['race_date', '年月日', None, '8', '9', '19', 'YYYYMMDD <-暫定版より順序'],
        ['horse_name', '馬名', None, '36', 'X', '27', '全角１８文字 <-入れ替え'],
        ['distance', '距離', None, '4', '9999', '63', None],
        ['surface_code', '芝ダ障害コード', None, '1', '9', '67', '1:芝, 2:ダート, 3:障害'],
        ['direction', '右左', None, '1', '9', '68', '1:右, 2:左, 3:直, 9:他'],
        ['course', '内外', None, '1', '9', '69', '1:通常(内), 2:外, 3,直ダ, 9:他'],
        ['track_condition', '馬場状態', None, '2', '99', '70', None],
        ['horse_sex', '種別', None, '2', '99', '72', '４歳以上等、→成績データの説明'],
        ['', '条件', None, '2', 'XX', '74', '900万下等、 →成績データの説明'],
        ['', '記号', None, '3', '999', '76', '○混等、 →成績データの説明'],
        ['', '重量', None, '1', '9', '79', 'ハンデ等、 →成績データの説明'],
        ['grade', 'グレード', None, '1', '9', '80', None],
        ['race_name', 'レース名', None, '50', 'X', '81', 'レース名の通称（全角２５文字）'],
        ['contender_count', '頭数', None, '2', '99', '131', None],
        ['race_name_short', 'レース名略称', None, '8', 'X', '133', '全角４文字'],
        ['order_of_finish', '着順', None, '2', '99', '141', None],
        ['', '異常区分', None, '1', '9', '143', None],
        ['', 'タイム', None, '4', '9999', '144', '1byte:分, 2-4byte:秒(0.1秒単位)'],
        ['mounted_weight', '斤量', None, '3', '999', '148', '0.1Kg単位'],
        ['jockey_name', '騎手名', None, '12', 'X', '151', '全角６文字'],
        ['trainer_name', '調教師名', None, '12', 'X', '163', '全角６文字'],
        ['final_win_odds', '確定単勝オッズ', None, '6', 'ZZZ9.9', '175', None],
        ['final_win_popularity', '確定単勝人気順位', None, '2', '99', '181', None],
        ['IDM', 'ＩＤＭ', None, '3', 'ZZ9', '183', None],
        ['', '素点', None, '3', 'ZZ9', '186', None],
        ['', '馬場差', None, '3', 'ZZ9', '189', None],
        ['pace', 'ペース', None, '3', 'ZZZ', '192', None],
        ['', '出遅', None, '3', 'ZZZ', '195', None],
        ['', '位置取', None, '3', 'ZZZ', '198', None],
        ['', '不利', None, '3', 'ZZZ', '201', None],
        ['', '前不利', None, '3', 'ZZZ', '204', '前３Ｆ内での不利'],
        ['', '中不利', None, '3', 'ZZZ', '207', '道中での不利'],
        ['', '後不利', None, '3', 'ZZZ', '210', '後３Ｆ内での不利'],
        ['', 'レース', None, '3', 'ZZZ', '213', None],
        ['', 'コース取り', None, '1', '9', '216', '1:最内,2:内,3:中,4:外,5:大外'],
        ['', '上昇度コード', None, '1', '9', '217', '1:AA, 2:A, 3:B, 4:C, 5:?'],
        ['', 'クラスコード', None, '2', '99', '218', None],
        ['', '馬体コード', None, '1', '9', '220', None],
        ['', '気配コード', None, '1', '9', '221', None],
        ['', 'レースペース', None, '1', 'X', '222', 'H:ハイ, M:平均, S:スロー'],
        ['', '馬ペース', None, '1', 'X', '223', '馬自身のペース(H:M:S)'],
        ['', 'テン指数', None, '5', 'ZZ9.9', '224', '前３Ｆタイムを指数化したもの'],
        ['', '上がり指数', None, '5', 'ZZ9.9', '229', '後３Ｆタイムを指数化したもの'],
        ['', 'ペース指数', None, '5', 'ZZ9.9', '234', '馬のペースを指数化したもの'],
        ['', 'レースＰ指数', None, '5', 'ZZ9.9', '239', 'レースのペースを指数化したもの'],
        ['', '1(2)着馬名', None, '12', 'X', '244', '全角６文字'],
        ['', '1(2)着タイム差', None, '3', '999', '256', '0.1秒単位'],
        ['', '前３Ｆタイム', None, '3', '999', '259', '0.1秒単位'],
        ['', '後３Ｆタイム', None, '3', '999', '262', '0.1秒単位'],
        ['comment', '備考', None, '24', 'X', '265', '全角１２文字（地方競馬場名等）'],
        ['reserved', '予備', None, '2', 'X', '289', 'スペース'],
        ['', '確定複勝オッズ下', None, '6', 'ZZZ9.9', '291', '最終的な複勝オッズ（下限）'],
        ['', '10時単勝オッズ', None, '6', 'ZZZ9.9', '297', '10時頃の単勝オッズ'],
        ['', '10時複勝オッズ', None, '6', 'ZZZ9.9', '303', '10時頃の複勝オッズ'],
        ['corner_1_pos', 'コーナー順位１', None, '2', '99', '309', None],
        ['corner_2_pos', 'コーナー順位２', None, '2', '99', '311', None],
        ['corner_3_pos', 'コーナー順位３', None, '2', '99', '313', None],
        ['corner_4_pos', 'コーナー順位４', None, '2', '99', '315', None],
        ['', '前３Ｆ先頭差', None, '3', '99', '317', '前３Ｆ地点での先頭とのタイム差'],
        ['', '後３Ｆ先頭差', None, '3', '99', '320', '後３Ｆ地点での先頭とのタイム差'],
        ['jockey_code', '騎手コード', None, '5', '9', '323', '騎手マスタとリンク'],
        ['trainer_code', '調教師コード', None, '5', '9', '328', '調教師マスタとリンク'],
        ['horse_weight', '馬体重', None, '3', '999', '333', 'データ無:スペース'],
        ['horse_weight_diff', '馬体重増減', None, '3', 'XZ9', '336', '符号+数字２桁、データ無:スペース'],
        ['weather_code', '天候コード', None, '1', '9', '339', 'コード表参照'],
        ['', 'コース', None, '1', 'X', '340', '1:A,2:A1,3:A2,4:B,5:C,6:D'],
        ['', 'レース脚質', None, '1', 'X', '341', '脚質コード参照'],
        ['win_odds', '単勝', None, '7', 'ZZZZZZ9', '342', '単位（円）'],
        ['', '複勝', None, '7', 'ZZZZZZ9', '349', '単位（円）'],
        ['', '本賞金', None, '5', 'ZZZZ9', '356', '単位（万円）'],
        ['', '収得賞金', None, '5', 'ZZZZ9', '361', '単位（万円）'],
        ['', 'レースペース流れ', None, '2', '99', '366', '→成績データの説明'],
        ['', '馬ペース流れ', None, '2', '99', '368', '→成績データの説明'],
        ['', '４角コース取り', None, '1', '9', '370', '1:最内,2:内,3:中,4:外,5:大外'],
        ['reserved', '予備', None, '4', 'X', '371', 'スペース'],
        ['newline', '改行', None, '2', 'X', '375', 'ＣＲ・ＬＦ']
    ]

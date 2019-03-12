from jrdb.templates.template import Template


class SED(Template):
    """
    http://www.jrdb.com/program/Sed/sed_doc.txt

    The "種別" values in the above document are incorrect.
    The correct values can be found [here](http://www.jrdb.com/program/jrdb_code.txt)
    """
    name = 'JRDB成績データ（SED）'
    items = [
        # レースキー
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['yr', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', None],
        ['race_num', 'Ｒ', None, '2', '99', '7', None],
        ['horse_num', '馬番', None, '2', '99', '9', None],
        ['pedigree_reg_num', '血統登録番号', None, '8', 'X', '11', None],
        ['race_date', '年月日', None, '8', '9', '19', 'YYYYMMDD <-暫定版より順序'],
        ['horse_name', '馬名', None, '36', 'X', '27', '全角１８文字 <-入れ替え'],
        # レース条件
        ['distance', '距離', None, '4', '9999', '63', None],
        ['surface_code', '芝ダ障害コード', None, '1', '9', '67', '1:芝, 2:ダート, 3:障害'],
        ['direction', '右左', None, '1', '9', '68', '1:右, 2:左, 3:直, 9:他'],
        ['course_inout', '内外', None, '1', '9', '69',
         '1:通常(内), 2:外, 3,直ダ, 9:他\n※障害のトラックは、以下の２通りとなります。\n"393":障害直線ダート\n"391":障害直線芝'],
        ['track_cond_code', '馬場状態', None, '2', '99', '70', None],
        ['race_category_code', '種別', None, '2', '99', '72', '４歳以上等、→成績データの説明'],
        ['race_cond_code', '条件', None, '2', 'XX', '74', '900万下等、 →成績データの説明'],
        ['race_symbols', '記号', None, '3', '999', '76', '○混等、 →成績データの説明'],
        ['impost_class_code', '重量', None, '1', '9', '79', 'ハンデ等、 →成績データの説明'],
        ['grade', 'グレード', None, '1', '9', '80', None],
        ['race_name', 'レース名', None, '50', 'X', '81', 'レース名の通称（全角２５文字）'],
        ['contender_count', '頭数', None, '2', '99', '131', None],
        ['race_name_abbr', 'レース名略称', None, '8', 'X', '133', '全角４文字'],
        # 馬成績
        ['order_of_finish', '着順', None, '2', '99', '141', None],
        ['penalty_code', '異常区分', None, '1', '9', '143', None],
        ['time', 'タイム', None, '4', '9999', '144', '1byte:分, 2-4byte:秒(0.1秒単位)'],
        ['mounted_weight', '斤量', None, '3', '999', '148', '0.1Kg単位'],
        ['jockey_name', '騎手名', None, '12', 'X', '151', '全角６文字'],
        ['trainer_name', '調教師名', None, '12', 'X', '163', '全角６文字'],
        ['fin_win_odds', '確定単勝オッズ', None, '6', 'ZZZ9.9', '175', None],
        ['fin_win_pop', '確定単勝人気順位', None, '2', '99', '181', None],
        # ＪＲＤＢデータ
        ['IDM', 'ＩＤＭ', None, '3', 'ZZ9', '183', None],
        ['raw_score', '素点', None, '3', 'ZZ9', '186', None],
        ['track_speed_shift', '馬場差', None, '3', 'ZZ9', '189', None],
        ['pace_ind', 'ペース', None, '3', 'ZZZ', '192', None],  # 単位/意味不明
        ['late_start_ind', '出遅', None, '3', 'ZZZ', '195', None],
        ['positioning', '位置取', None, '3', 'ZZZ', '198', None],  # 単位/意味不明
        ['disad_ind', '不利', None, '3', 'ZZZ', '201', None],  # 単位不明
        ['beg_3F_disad_ind', '前不利', None, '3', 'ZZZ', '204', '前３Ｆ内での不利'],
        ['mid_3F_disad_ind', '中不利', None, '3', 'ZZZ', '207', '道中での不利'],
        ['end_3F_disad_ind', '後不利', None, '3', 'ZZZ', '210', '後３Ｆ内での不利'],
        ['race_ind', 'レース', None, '3', 'ZZZ', '213', None],  # 単位/意味不明
        ['race_line', 'コース取り', None, '1', '9', '216', '1:最内,2:内,3:中,4:外,5:大外'],
        ['improvement_code', '上昇度コード', None, '1', '9', '217', '1:AA, 2:A, 3:B, 4:C, 5:?'],
        ['race_class_code', 'クラスコード', None, '2', '99', '218', None],
        ['horse_body_code', '馬体コード', None, '1', '9', '220', None],
        ['horse_cond_code', '気配コード', None, '1', '9', '221', None],
        ['race_pace', 'レースペース', None, '1', 'X', '222', 'H:ハイ, M:平均, S:スロー'],
        ['horse_pace', '馬ペース', None, '1', 'X', '223', '馬自身のペース(H:M:S)'],
        ['beg_3F_time_ind', 'テン指数', None, '5', 'ZZ9.9', '224', '前３Ｆタイムを指数化したもの'],
        ['end_3F_time_ind', '上がり指数', None, '5', 'ZZ9.9', '229', '後３Ｆタイムを指数化したもの'],
        # ペース指数とは、各馬のスタートから残り３Ｆ地点までの時計を指数化したものです
        ['pace_ind', 'ペース指数', None, '5', 'ZZ9.9', '234', '馬のペースを指数化したもの'],
        ['race_pace_ind', 'レースＰ指数', None, '5', 'ZZ9.9', '239', 'レースのペースを指数化したもの'],
        # for 1st place horses, the second place horse name/time
        # for 2nd > place horses, the first place horse name/time
        ['fos_horse_name', '1(2)着馬名', None, '12', 'X', '244', '全角６文字'],
        ['fos_horse_time_diff', '1(2)着タイム差', None, '3', '999', '256', '0.1秒単位'],
        ['beg_3F_time', '前３Ｆタイム', None, '3', '999', '259', '0.1秒単位'],
        ['end_3F_time', '後３Ｆタイム', None, '3', '999', '262', '0.1秒単位'],
        ['comment', '備考', None, '24', 'X', '265', '全角１２文字（地方競馬場名等）'],
        ['reserved_0', '予備', None, '2', 'X', '289', 'スペース'],
        ['fin_show_odds_lower_limit', '確定複勝オッズ下', None, '6', 'ZZZ9.9', '291', '最終的な複勝オッズ（下限）'],
        ['win_odds_10am', '10時単勝オッズ', None, '6', 'ZZZ9.9', '297', '10時頃の単勝オッズ'],
        ['show_odds_10am', '10時複勝オッズ', None, '6', 'ZZZ9.9', '303', '10時頃の複勝オッズ'],
        ['cor_1_pos', 'コーナー順位１', None, '2', '99', '309', None],
        ['cor_2_pos', 'コーナー順位２', None, '2', '99', '311', None],
        ['cor_3_pos', 'コーナー順位３', None, '2', '99', '313', None],
        ['cor_4_pos', 'コーナー順位４', None, '2', '99', '315', None],
        ['beg_3F_1p_time_diff', '前３Ｆ先頭差', None, '3', '99', '317', '前３Ｆ地点での先頭とのタイム差'],
        ['end_3F_1P_time_diff', '後３Ｆ先頭差', None, '3', '99', '320', '後３Ｆ地点での先頭とのタイム差'],
        ['jockey_code', '騎手コード', None, '5', '9', '323', '騎手マスタとリンク'],
        ['trainer_code', '調教師コード', None, '5', '9', '328', '調教師マスタとリンク'],
        ['horse_weight', '馬体重', None, '3', '999', '333', 'データ無:スペース'],
        ['horse_weight_diff', '馬体重増減', None, '3', 'XZ9', '336', '符号+数字２桁、データ無:スペース'],
        ['weather_code', '天候コード', None, '1', '9', '339', 'コード表参照'],
        ['course_label', 'コース', None, '1', 'X', '340', '1:A,2:A1,3:A2,4:B,5:C,6:D'],
        ['running_style_code', 'レース脚質', None, '1', 'X', '341', '脚質コード参照'],
        ['win_payoff_yen', '単勝', None, '7', 'ZZZZZZ9', '342', '単位（円）'],
        ['show_payoff_yen', '複勝', None, '7', 'ZZZZZZ9', '349', '単位（円）'],
        ['purse', '本賞金', None, '5', 'ZZZZ9', '356', '単位（万円）'],
        ['p1_prize', '収得賞金', None, '5', 'ZZZZ9', '361', '単位（万円）'],
        ['race_pace_flow_code', 'レースペース流れ', None, '2', '99', '366', '→成績データの説明'],
        ['horse_pace_flow_code', '馬ペース流れ', None, '2', '99', '368', '→成績データの説明'],
        ['cor_4_race_line', '４角コース取り', None, '1', '9', '370', '1:最内,2:内,3:中,4:外,5:大外'],
        ['reserved_1', '予備', None, '4', 'X', '371', 'スペース'],
        ['newline', '改行', None, '2', 'X', '375', 'ＣＲ・ＬＦ']
    ]

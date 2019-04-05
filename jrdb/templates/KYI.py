from jrdb.templates.template import Template


class KYI(Template):
    """
    http://www.jrdb.com/program/Kyi/kyi_doc.txt
    http://www.jrdb.com/program/Kyi/ky_siyo_doc.txt
    """
    name = 'JRDB競走馬データ（KYI）'
    items = [
        # レースキー
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['yr', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', '16進数(数字 or 小文字アルファベット)'],
        ['race_num', 'Ｒ', None, '2', '99', '7', None],
        ['horse_num', '馬番', None, '2', '99', '9', None],
        ['pedigree_reg_num', '血統登録番号', None, '8', 'X', '11', None],
        ['horse_name', '馬名', None, '36', 'X', '19', '全角１８文字'],

        ['IDM', 'ＩＤＭ', None, '5', 'ZZ9.9', '55', None],
        ['jockey_index', '騎手指数', None, '5', 'ZZ9.9', '60', None],
        ['info_index', '情報指数', None, '5', 'ZZ9.9', '65', None],
        ['reserved_1', '予備１', None, '5', 'ZZ9.9', '70', '将来拡張用'],
        ['reserved_2', '予備２', None, '5', 'ZZ9.9', '75', '将来拡張用'],
        ['reserved_3', '予備３', None, '5', 'ZZ9.9', '80', '将来拡張用'],
        ['total_index', '総合指数', None, '5', 'ZZ9.9', '85', None],

        ['running_style', '脚質', None, '1', '9', '90', None],
        ['distance_aptitude', '距離適性', None, '1', '9', '91', None],
        ['improvement', '上昇度', None, '1', '9', '92', None],
        ['rotation', 'ローテーション', None, '3', 'ZZ9', '93', '間に金曜日が入っている数で決定、連闘は０、初出走はスペースとなる'],

        ['odds_win_base', '基準オッズ', None, '5', 'ZZ9.9', '96', None],
        ['popularity_win_base', '基準人気順位', None, '2', 'Z9', '101', None],
        ['odds_show_win', '基準複勝オッズ', None, '5', 'ZZ9.9', '103', None],
        ['popularity_show_base', '基準複勝人気順位', None, '2', 'Z9', '108', None],
        ['journal_mark_special_c_dbl', '特定情報◎', None, '3', 'ZZ9', '110', '情報・専門紙の印数（特定）'],
        ['journal_mark_special_c', '特定情報○', None, '3', 'ZZ9', '113', None],
        ['journal_mark_special_t_dark', '特定情報▲', None, '3', 'ZZ9', '116', None],
        ['journal_mark_special_t', '特定情報△', None, '3', 'ZZ9', '119', None],
        ['journal_mark_special_x', '特定情報×', None, '3', 'ZZ9', '122', None],
        ['journal_mark_total_c_dbl', '総合情報◎', None, '3', 'ZZ9', '125', '情報・専門紙の印数（総合）'],
        ['journal_mark_total_c', '総合情報○', None, '3', 'ZZ9', '128', None],
        ['journal_mark_total_t_dark', '総合情報▲', None, '3', 'ZZ9', '131', None],
        ['journal_mark_total_t', '総合情報△', None, '3', 'ZZ9', '134', None],
        ['journal_mark_total_x', '総合情報×', None, '3', 'ZZ9', '137', None],
        ['popularity_index', '人気指数', None, '5', 'ZZZZ9', '140', '第２版で変更'],
        ['trainer_index', '調教指数', None, '5', 'ZZ9.9', '145', None],
        ['stable_index', '厩舎指数', None, '5', 'ZZ9.9', '150', None],
        # ===以下第３版にて追加===
        ['trainer_horse_evaluation', '調教矢印コード', None, '1', '9', '155', None],
        ['stable_horse_evaluation', '厩舎評価コード', None, '1', '9', '156', None],
        # 騎手Ａが単勝基準オッズＢの馬に乗った場合の過去の成績を集計し、算出された連対率を騎手期待連対率としています。
        ['jockey_exp_1or2_place_rate', '騎手期待連対率', None, '4', 'Z9.9', '157', None],
        # ＪＲＤＢでの穴馬分析は激走指数
        ['flat_out_run_index', '激走指数', None, '3', 'ZZ9', '161', None],
        ['paddock_observed_hoof', '蹄コード', None, '2', '99', '164', None],
        ['yielding_track_aptitude', '重適正コード', None, '1', '9', '166', None],
        ['race_class', 'クラスコード', None, '2', '99', '167', None],
        ['reserved_4', '予備', None, '2', 'X', '169', 'スペース'],
        # ===以下第４版にて追加===
        ['blinker_usage', 'ブリンカー', None, '1', 'X', '171', '1:初装着,2:再装着,3:ブリンカ'],
        ['jockey_name', '騎手名', None, '12', 'X', '172', '全角６文字'],
        ['weight_carried', '負担重量', None, '3', '999', '184', '0.1Kg単位'],
        ['trainee_cat', '見習い区分', None, '1', '9', '187', '1:☆(1K減),2:△(2K減),3:▲(3K減)'],
        ['trainer_name', '調教師名', None, '12', 'X', '188', '全角６文字'],
        ['trainer_area', '調教師所属', None, '4', 'X', '200', '全角２文字'],
        # 他データリンク用キー
        ['', '前走１競走成績キー', None, '16', '9', '204', None],  # IGNORED
        ['', '前走２競走成績キー', None, '16', '9', '220', None],  # IGNORED
        ['', '前走３競走成績キー', None, '16', '9', '236', None],  # IGNORED
        ['', '前走４競走成績キー', None, '16', '9', '252', None],  # IGNORED
        ['', '前走５競走成績キー', None, '16', '9', '268', None],  # IGNORED
        ['', '前走１レースキー', None, '8', '9', '284', None],  # IGNORED
        ['', '前走２レースキー', None, '8', '9', '292', None],  # IGNORED
        ['', '前走３レースキー', None, '8', '9', '300', None],  # IGNORED
        ['', '前走４レースキー', None, '8', '9', '308', None],  # IGNORED
        ['', '前走５レースキー', None, '8', '9', '316', None],  # IGNORED
        ['post_position', '枠番', None, '1', '9', '324', None],
        ['reserved_5', '予備', None, '2', 'X', '325', 'スペース'],
        # ===以下第５版にて追加===
        # 印コード
        ['overall_mark', '総合印', None, '1', '9', '327', '印コード'],
        ['IDM_mark', 'ＩＤＭ印', None, '1', '9', '328', '印コード'],
        ['info_mark', '情報印', None, '1', '9', '329', '印コード'],
        ['jockey_mark', '騎手印', None, '1', '9', '330', '印コード'],
        ['stable_mark', '厩舎印', None, '1', '9', '331', '印コード'],
        ['trainer_mark', '調教印', None, '1', '9', '332', '印コード'],
        ['flat_out_run_mark', '激走印', None, '1', '9', '333', '1:激走馬'],
        ['turf_aptitude_mark', '芝適性コード', None, '1', 'X', '334', '1:◎, 2:○, 3:△'],
        ['dirt_aptitude_mark', 'ダ適性コード', None, '1', 'X', '335', '1:◎, 2:○, 3:△'],
        ['jockey_code', '騎手コード', None, '5', '9', '336', '騎手マスタとリンク'],
        ['trainer_code', '調教師コード', None, '5', '9', '341', '調教師マスタとリンク'],
        ['reserved_6', '予備', None, '1', 'X', '346', 'スペース'],
        # ===以下第６版にて追加===
        # 賞金情報
        ['', '獲得賞金', None, '6', 'ZZZZZ9', '347', '単位万円(含む付加賞)'],
        ['p1_prize', '収得賞金', None, '5', 'ZZZZ9', '353', '単位万円'],
        ['race_condition_group_code', '条件クラス', None, '1', '9', '358', '条件グループコード参照\n収得賞金から出走できるクラス'],

        # 展開予想データ
        ['b3f_time_index', 'テン指数', None, '5', 'ZZZ.9', '359', '予想テン指数'],
        ['pace_index', 'ペース指数', None, '5', 'ZZZ.9', '364', '予想ペース指数'],
        ['f3f_time_index', '上がり指数', None, '5', 'ZZZ.9', '369', '予想上がり指数'],
        ['positioning_index', '位置指数', None, '5', 'ZZZ.9', '374', '予想位置指数'],
        ['pace', 'ペース予想', None, '1', 'X', '379', 'H,M,S'],
        ['mid_race_position', '道中順位', None, '2', 'Z9', '380', None],
        ['mid_race_margin', '道中差', None, '2', 'Z9', '382', '半馬身(約0.1秒)単位'],
        ['mid_race_in_out', '道中内外', None, '1', '9', '384', '2:内 ～ 4:外'],
        ['f3f_position', '後３Ｆ順位', None, '2', 'Z9', '385', None],
        ['f3f_margin', '後３Ｆ差', None, '2', 'Z9', '387', '半馬身(約0.1秒)単位'],
        ['f3f_in_out', '後３Ｆ内外', None, '1', '9', '389', '2:内 ～ 5:大外'],
        ['goal_position', 'ゴール順位', None, '2', 'Z9', '390', None],
        ['goal_margin', 'ゴール差', None, '2', 'Z9', '392', '半馬身(約0.1秒)単位'],
        ['goal_in_out', 'ゴール内外', None, '1', '9', '394', '1:最内 ～ 5:大外'],
        ['race_development_symbol', '展開記号', None, '1', 'X', '395', '展開記号コード参照'],
        # ===以下第６a版にて追加===
        ['distance_aptitude_2', '距離適性２', None, '1', '9', '396', None],  # 意味不明
        ['weight_pp_decision', '枠確定馬体重', None, '3', '999', '397', 'データ無:スペース'],
        ['weight_diff_pp_decision', '枠確定馬体重増減', None, '3', 'XZ9', '400', '符号+数字２桁,データ無:スペース'],
        # ===以下第７版にて追加===
        ['is_cancelled', '取消フラグ', None, '1', '9', '403', '1:取消'],
        ['sex', '性別コード', None, '1', '9', '404', '1:牡,2:牝,3,セン'],
        ['owner_name', '馬主名', None, '40', 'X', '405', '全角２０文字'],
        ['owner_racetrack_code', '馬主会コード', None, '2', '99', '445', '参考データ。'],
        ['horse_symbol', '馬記号コード', None, '2', '99', '447', 'コード表参照'],
        ['flat_out_run_position', '激走順位', None, '2', 'Z9', '449', 'レース出走馬中での順位'],
        ['LS_index_position', 'LS指数順位', None, '2', 'Z9', '451', None],
        ['b3f_index_position', 'テン指数順位', None, '2', 'Z9', '453', None],
        ['pace_index_position', 'ペース指数順位', None, '2', 'Z9', '455', None],
        ['f3f_index_position', '上がり指数順位', None, '2', 'Z9', '457', None],
        ['positioning_index_position', '位置指数順位', None, '2', 'Z9', '459', None],
        # ===以下第８版にて追加===
        ['jockey_exp_win_rate', '騎手期待単勝率', None, '4', 'Z9.9', '461', None],
        ['jockey_exp_show_rate', '騎手期待３着内率', None, '4', 'Z9.9', '465', None],
        ['transport_category', '輸送区分', None, '1', 'X', '469', None],
        # ===以下第９版にて追加===
        ['', '走法', None, '8', '9', '470', 'コード表参照'],  # IGNORED (走法データの採取は休止)
        ['figure', '体型', None, '24', 'X', '478', 'コード表参照'],
        ['figure_overall_1', '体型総合１', None, '3', '9', '502', '特記コード参照'],  # special_mention_code
        ['figure_overall_2', '体型総合２', None, '3', '9', '505', '特記コード参照'],
        ['figure_overall_3', '体型総合３', None, '3', '9', '508', '特記コード参照'],
        ['horse_special_mention_1', '馬特記１', None, '3', '9', '511', '特記コード参照'],
        ['horse_special_mention_2', '馬特記２', None, '3', '9', '514', '特記コード参照'],
        ['horse_special_mention_3', '馬特記３', None, '3', '9', '517', '特記コード参照'],
        # 展開参考データ
        ['horse_start_index', '馬スタート指数', None, '4', 'Z9.9', '520', None],
        ['late_start_rate', '馬出遅率', None, '4', 'Z9.9', '524', None],
        ['', '参考前走', None, '2', '99', '528', '参考となる前走（２走分格納）'],  # 1, 2, 3など（意味不明）
        ['', '参考前走騎手コード', None, '5', 'X', '530', '参考となる前走の騎手'],  # 同上
        ['big_bet_index', '万券指数', None, '3', 'ZZ9', '535', None],
        ['big_bet_symbol', '万券印', None, '1', '9', '538', None],
        # ===以下第10版にて追加===
        ['rank_lowered', '降級フラグ', None, '1', '9', '539', '1:降級, 2:２段階降級, 0:通常'],
        ['flat_out_run_type', '激走タイプ', None, '2', 'XX', '540', '激走馬のタイプ分け。説明参照'],
        ['rest_reason_code', '休養理由分類コード', None, '2', '99', '542', 'コード表参照'],
        # ===以下第11版にて追加===
        ['flags', 'フラグ', None, '16', 'X', '544', '初芝初ダ初障などのフラグ'],
        ['nth_race_since_training_start', '入厩何走目', None, '2', 'Z9', '560', '例）2:入厩後２走目'],
        ['training_start_date', '入厩年月日', None, '8', '9', '562', 'YYYYMMDD'],
        ['nth_day_since_training_start', '入厩何日前', None, '3', 'ZZ9', '570', 'レース日から遡っての入厩の日数'],
        ['pasture_name', '放牧先', None, '50', 'X', '573', '放牧先/近走放牧先'],
        ['pasture_rank', '放牧先ランク', None, '1', 'X', '623', 'A-E'],
        ['stable_rank', '厩舎ランク', None, '1', '9', '624', '高い1-9低い 内容説明参照'],
        ['reserved_7', '予備', None, '398', 'X', '625', 'スペース'],
        ['newline', '改行', None, '2', 'X', '1023', 'ＣＲ・ＬＦ']
    ]

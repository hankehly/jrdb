from jrdb.templates.template import Template


class KAB(Template):
    """
    http://www.jrdb.com/program/Kab/kab_doc.txt

    010821200809133土札幌11 222-2 -10 0 0 0 1 111-7 49 214  000
    060841200809131土中山11 111-12-3-2-10 0 1 111-1241 110  007.5
    """
    name = 'JRDB開催データ（KAB）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['yr', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', None],
        ['date', '年月日', None, '8', '9', '7', 'YYYYMMDD'],
        ['host_category', '開催区分', None, '1', '9', '15', '1:関東, 2:関西, 3:ローカル'],
        ['weekday', '曜日', None, '2', 'X', '16', '日－土'],
        ['racetrack_name', '場名', None, '4', 'X', '18', '競馬場名'],
        ['weather_code', '天候コード', None, '1', '9', '22', '推 →JRDBデータコード表'],
        ['turf_track_condition_code', '芝馬場状態コード', None, '2', '9', '23', '推 →JRDBデータコード表'],
        ['turf_track_condition_inner', '芝馬場状態内', None, '1', '9', '25', '推 1:絶好, 2:良, 3,稍荒, 4:荒'],
        ['turf_track_condition_middle', '芝馬場状態中', None, '1', '9', '26', '推 1:絶好, 2:良, 3,稍荒, 4:荒'],
        ['turf_track_condition_outer', '芝馬場状態外', None, '1', '9', '27', '推 1:絶好, 2:良, 3,稍荒, 4:荒'],
        ['turf_track_speed_shift', '芝馬場差', None, '3', '9', '28', '推'],
        ['hs_track_speed_shift__innermost', '直線馬場差最内', None, '2', '99', '31', '推'],
        ['hs_track_speed_shift__inner', '直線馬場差内', None, '2', '99', '33', '推'],
        ['hs_track_speed_shift__middle', '直線馬場差中', None, '2', '99', '35', '推'],
        ['hs_track_speed_shift__outer', '直線馬場差外', None, '2', '99', '37', '推'],
        ['hs_track_speed_shift__outermost', '直線馬場差大外', None, '2', '99', '39', '推'],
        ['dirt_track_condition_code', 'ダ馬場状態コード', None, '2', '9', '41', '推 →JRDBデータコード表'],
        ['dirt_track_condition_inner', 'ダ馬場状態内', None, '1', '9', '43', '推 1:絶好, 2:良, 3,稍荒, 4:荒'],
        ['dirt_track_condition_middle', 'ダ馬場状態中', None, '1', '9', '44', '推 1:絶好, 2:良, 3,稍荒, 4:荒'],
        ['dirt_track_condition_outer', 'ダ馬場状態外', None, '1', '9', '45', '推 1:絶好, 2:良, 3,稍荒, 4:荒'],
        ['dirt_track_speed_shift', 'ダ馬場差', None, '3', '9', '46', '推'],
        ['data_category_1', 'データ区分', None, '1', '9', '49', '1:特別登録,2:想定確定,3:枠確定,4:前日'],
        ['nth_occurrence', '連続何日目', None, '2', '9', '50', '日数'],
        ['turf_type', '芝種類', None, '1', 'X', '52', '1:野芝, 2:洋芝, 3:混生'],
        ['grass_height', '草丈', None, '4', 'Z9.9', '53', '単位cm'],
        ['used_rolling_compactor', '転圧', None, '1', 'X', '57', '1:転圧, 0:無し'],
        ['used_anti_freeze_agent', '凍結防止剤', None, '1', 'X', '58', '1:凍結防止剤散布, 0:無し'],
        ['mm_precipitation', '中間降水量', None, '5', 'ZZ9.9', '59', '単位mm'],
        ['reserved', '予備', None, '7', 'X', '64', 'スペース'],
        ['newline', '改行', None, '2', 'X', '71', 'ＣＲ・ＬＦ'],
        ['data_category_2', 'データ区分', None, '1', '9', '49', '1:特別登録,2:想定確定,3前日'],
        ['data_category_3', 'データ区分', None, '1', '9', '49', '1:特別登録,2:想定確定,3:枠確定,4:前日']
    ]

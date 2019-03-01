from jrdb.templates.template import Template

"""
調教量についての評価です。
"""
TRAINING_AMOUNT = {
    'A': '多い',
    'B': '普通',
    'C': '少ない',
    'D': '非常に少ない',
}

"""
仕上指数変化（参考値）
前走（中央競馬のレース出走時）の仕上指数との比較です。
"""
TRAINING_RESULT_INDICATOR_CHANGE = {
    1: '++(攻め強化大)',
    2: '+ (攻め強化)',
    3: '  (平行線)',
    4: '- (攻め弱化)',
}


class CYB(Template):
    """
    http://www.jrdb.com/program/Cyb/cyb_doc.txt
    """
    name = 'JRDB調教分析データ（CYB）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['year', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', None],
        ['race_number', 'Ｒ', None, '2', '99', '7', None],
        ['horse_number', '馬番', None, '2', '99', '9', None],
        ['training_style', '調教タイプ', None, '2', 'X', '11', '調教タイプをコード化※1'],
        ['training_course_category', '調教コース種別', None, '1', 'X', '13', '調教コース種別をコード化※1'],
        # 調教コース種類 01:有り, 00:無し
        ['trained_hill', '坂', None, '2', '99', '14', '（坂路）'],
        ['trained_wood_chip', 'Ｗ', None, '2', '99', '16', '（ウッドコース）'],
        ['trained_dirt', 'ダ', None, '2', '99', '18', '（ダートコース）'],
        ['trained_turf', '芝', None, '2', '99', '20', '（芝コース）'],
        ['trained_pool', 'プ', None, '2', '99', '22', '（プール調教）'],
        ['trained_obstacle', '障', None, '2', '99', '24', '（障害練習）'],
        ['trained_poly_track', 'ポ', None, '2', '99', '26', '（ポリトラック）第２版で追加'],
        ['training_distance', '調教距離', None, '1', 'X', '28', '1:長め,2:普通,3:短め,4:2本,0:他'],
        ['training_emphasis', '調教重点', None, '1', 'X', '29', '1:テン,2:中間,3:終い,4:平均,0:他'],
        # 本追い切りの時計を指数化。馬場差、回り位置、乗り役、距離、調教過程で補正しています。
        # この指数の基準は「条件クラス馬の一杯追い切り」を"60"としています。
        ['warm_up_time_indicator', '追切指数', None, '3', 'ZZ9', '30', '調教時計を指数化（参考） ※1'],
        # 追切指数をベースに、前走の状態、ローテーション、調教過程、調教量から分析した馬の仕上り具合を表します。
        # この指数の基準も追切指数と同様で「条件クラス馬の一杯追い切り」を"60"としています。
        ['training_result_indicator', '仕上指数', None, '3', 'ZZ9', '33', '仕上り状態を指数化（参考）※1'],
        ['training_amount', '調教量評価', None, '1', 'X', '36', 'A,B,C,Dに分類 ※1'],
        ['training_result_indicator_change', '仕上指数変化', None, '1', 'X', '37', '※1'],
        ['training_comment', '調教コメント', None, '40', 'X', '38', '※2'],
        ['training_comment_date', 'コメント年月日', None, '8', 'X', '78', 'コメントの対象となった調教日'],
        ['training_evaluation', '調教評価', None, '1', 'X', '86', '３段階評価 1:◎, 2:○, 3:△'],
        ['reserved', '予備', None, '8', 'X', '87', 'スペース'],
        ['newline', '改行', None, '2', 'X', '95', 'ＣＲ・ＬＦ']
    ]

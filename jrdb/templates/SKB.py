from jrdb.models import Racetrack, SpecialMentionCode
from jrdb.templates.template import Template


class SKB(Template):
    """
    http://www.jrdb.com/program/Skb/skb_doc.txt
    """
    name = 'JRDB成績拡張データ（SKB）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['yr', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', '16進数(数字 or 小文字アルファベット)'],
        ['race_num', 'Ｒ', None, '2', '99', '7', None],
        ['num', '馬番', None, '2', '99', '9', None],
        ['pedigree_reg_num', '血統登録番号', None, '8', 'X', '11', None],
        ['race_date', '年月日', None, '8', '9', '19', 'YYYYMMDD'],  # IGNORED (use value from BAC)
        ['special_mention_code', '特記コード', '6', '3', '999', '27', '特記コード表参照 ※1'],
        ['horse_gear_code', '馬具コード', '8', '3', '999', '45', '馬具コード表参照 ※1 ※3'],
        ['hoof_code_overall', '総合', '3', '3', '999', '69', None],
        ['hoof_code_front_left', '左前', '3', '3', '999', '78', None],
        ['hoof_code_front_right', '右前', '3', '3', '999', '87', None],
        ['hoof_code_back_left', '左後', '3', '3', '999', '96', None],
        ['hoof_code_back_right', '右後', '3', '3', '999', '105', None],
        ['paddock_comment', 'パドックコメント', None, '40', 'X', '114', '全角半角混在'],
        ['hoof_comment', '脚元コメント', None, '40', 'X', '154', '全角半角混在'],
        ['horse_gear_or_other_comment', '馬具(その他)コメント', None, '40', 'X', '194', '全角半角混在'],
        ['race_comment', 'レースコメント', None, '40', 'X', '234', '全角半角混在'],
        ['bit', 'ハミ', None, '3', '999', '274', '馬具コード表参照 ※5'],
        ['bandage', 'バンテージ', None, '3', '999', '277', '007:バンテージ'],
        ['horseshoe', '蹄鉄', None, '3', '999', '280', '馬具コード表参照 ※5'],
        ['hoof_condition', '蹄状態', None, '3', '999', '283', '馬具コード表参照 ※5'],
        ['periostitis', 'ソエ', None, '3', '999', '286', '馬具コード表参照 ※5'],
        ['exostosis', '骨瘤', None, '3', '999', '289', '馬具コード表参照 ※5'],
        ['reserved', '予備', None, '11', 'X', '292', 'スペース'],
        ['newline', '改行', None, '2', 'X', '303', 'ＣＲ・ＬＦ']
    ]

    def clean(self):
        racetracks = Racetrack.objects.filter(code__in=self.df.racetrack_code).values('code', 'id')
        s = self.df.racetrack_code.map({racetrack['code']: racetrack['id'] for racetrack in racetracks})
        s.name = 'racetrack_id'

        df = s.to_frame()
        df['yr'] = self.df.yr.astype(int)
        df['round'] = self.df['round'].astype(int)
        df['day'] = self.df.day.str.strip()
        df['num'] = self.df.race_num.astype(int)
        df['special_mention_id'] = SpecialMentionCode.key2id(self.df.special_mention_code)

        df['horse_pedigree_reg_num'] = self.df.pedigree_reg_num

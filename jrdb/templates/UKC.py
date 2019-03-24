from django.db import IntegrityError

from jrdb.models import Horse, Racetrack
from jrdb.models.choices import SEX, HAIR_COLOR, HORSE_SYMBOL
from jrdb.templates.parse import parse_date, parse_int_or, filter_na
from jrdb.templates.template import Template

import numpy as np


class UKC(Template):
    """
    http://www.jrdb.com/program/Ukc/ukc_doc.txt
    """
    name = 'JRDB馬基本データ（UKC）'
    items = [
        ['pedigree_reg_num', '血統登録番号', None, '8', 'X', '1', None],
        ['name', '馬名', None, '36', 'X', '9', '全角１８文字'],
        ['sex', '性別コード', None, '1', '9', '45', '1:牡,2:牝,3,セン'],
        ['hair_color_code', '毛色コード', None, '2', '9', '46', 'コード表参照'],
        ['horse_symbol', '馬記号コード', None, '2', '9', '48', 'コード表参照'],
        ['sire_name', '父馬名', None, '36', 'X', '50', '全角１８文字'],
        ['dam_name', '母馬名', None, '36', 'X', '86', '全角１８文字'],
        ['damsire_name', '母父馬名', None, '36', 'X', '122', '全角１８文字'],
        ['birthday', '生年月日', None, '8', '9', '158', 'YYYYMMDD'],
        ['sire_birth_yr', '父馬生年', None, '4', '9', '166', 'YYYY 血統キー用'],
        ['dam_birth_yr', '母馬生年', None, '4', '9', '170', 'YYYY 血統キー用'],
        ['damsire_birth_yr', '母父馬生年', None, '4', '9', '174', 'YYYY 血統キー用'],
        ['owner_name', '馬主名', None, '40', 'X', '178', '全角２０文字'],
        ['owner_racetrack_code', '馬主会コード', None, '2', '99', '218', '競馬場毎にある。場コードと同じ'],
        ['breeder_name', '生産者名', None, '40', 'X', '220', '全角２０文字'],
        ['breeding_loc_name', '産地名', None, '8', 'X', '260', '全角４文字'],
        ['is_retired', '登録抹消フラグ', None, '1', '9', '268', '0:現役,1:抹消'],
        ['jrdb_saved_on', 'データ年月日', None, '8', '9', '269', 'YYYYMMDD'],  # same as filename date
        ['sire_genealogy_code', '父系統コード', None, '4', '9', '277', None],
        ['damsire_genealogy_code', '母父系統コード', None, '4', '9', '281', None],
        ['reserved', '予備', None, '6', 'X', '285', 'スペース'],
        ['newline', '改行', None, '2', 'X', '291', 'ＣＲ・ＬＦ']
    ]

    def clean(self):
        df = self.df.pedigree_reg_num.to_frame()

        df['name'] = self.df.name.str.strip()
        df['sex'] = self.df.sex.map(SEX.get_key_map())
        df['hair_color'] = self.df.hair_color_code.map(HAIR_COLOR.get_key_map())
        df['symbol'] = self.df.horse_symbol.map(HORSE_SYMBOL.get_key_map())
        df['sire_name'] = self.df.sire_name.str.strip()
        df['dam_name'] = self.df.dam_name.str.strip()
        df['damsire_name'] = self.df.damsire_name.str.strip()
        df['birthday'] = self.df.birthday.apply(parse_date, args=('%Y%m%d',))

        df['sire_birth_yr'] = self.df.sire_birth_yr.str.strip() \
            .apply(parse_int_or, args=(np.nan,)) \
            .astype('Int64')

        df['dam_birth_yr'] = self.df.dam_birth_yr.str.strip() \
            .apply(parse_int_or, args=(np.nan,)) \
            .astype('Int64')

        df['damsire_birth_yr'] = self.df.damsire_birth_yr.str.strip() \
            .apply(parse_int_or, args=(np.nan,)) \
            .astype('Int64')

        df['owner_name'] = self.df.owner_name.str.strip()

        racetracks = Racetrack.objects.filter(code__in=self.df.owner_racetrack_code)
        racetrack_map = {racetrack.code: racetrack.id for racetrack in racetracks}
        df['owner_racetrack_id'] = self.df.owner_racetrack_code.map(racetrack_map).astype('Int64')

        df['breeder_name'] = self.df.breeder_name.str.strip()
        df['breeding_loc_name'] = self.df.breeding_loc_name.str.strip()
        df['is_retired'] = self.df.is_retired.astype(int).astype(bool)
        df['sire_genealogy_code'] = self.df.sire_genealogy_code.str.strip()
        df['damsire_genealogy_code'] = self.df.damsire_genealogy_code.str.strip()

        df['jrdb_saved_on'] = self.df.jrdb_saved_on.apply(parse_date, args=('%Y%m%d',))

        return df

    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            obj = filter_na(row)
            try:
                Horse.objects.create(**obj)
            except IntegrityError:
                horse = Horse.objects.get(pedigree_reg_num=obj['pedigree_reg_num'])
                if horse.jrdb_saved_on is None or obj['jrdb_saved_on'] >= horse.jrdb_saved_on:
                    for name, value in obj.items():
                        setattr(horse, name, value)
                    horse.save()

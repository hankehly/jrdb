from jrdb.datadocs.template import Template


class UKC(Template):
    name = 'JRDB馬基本データ（UKC）'
    items = [
        ['pedigree_registration_number', '血統登録番号', None, '8', 'X', '1', None],
        ['horse_name', '馬名', None, '36', 'X', '9', '全角１８文字'],
        ['sex_code', '性別コード', None, '1', '9', '45', '1:牡,2:牝,3,セン'],
        ['hair_color_code', '毛色コード', None, '2', '9', '46', 'コード表参照'],
        ['horse_symbol', '馬記号コード', None, '2', '9', '48', 'コード表参照'],
        ['sire_name', '父馬名', None, '36', 'X', '50', '全角１８文字'],
        ['dam_name', '母馬名', None, '36', 'X', '86', '全角１８文字'],
        ['damsire_name', '母父馬名', None, '36', 'X', '122', '全角１８文字'],
        ['birthday', '生年月日', None, '8', '9', '158', 'YYYYMMDD'],
        ['sire_birth_year', '父馬生年', None, '4', '9', '166', 'YYYY 血統キー用'],
        ['dam_birth_year', '母馬生年', None, '4', '9', '170', 'YYYY 血統キー用'],
        ['damsire_birth_year', '母父馬生年', None, '4', '9', '174', 'YYYY 血統キー用'],
        ['owner_name', '馬主名', None, '40', 'X', '178', '全角２０文字'],
        ['owners_association_code', '馬主会コード', None, '2', '99', '218', '競馬場毎にある。場コードと同じ'],
        ['breeder_name', '生産者名', None, '40', 'X', '220', '全角２０文字'],
        ['breeding_location_name', '産地名', None, '8', 'X', '260', '全角４文字'],
        ['deregistration_flag', '登録抹消フラグ', None, '1', '9', '268', '0:現役,1:抹消'],
        ['data_saved_on', 'データ年月日', None, '8', '9', '269', 'YYYYMMDD'],  # same as filename date
        ['sire_genealogy_code', '父系統コード', None, '4', '9', '277', None],
        ['damsire_genealogy_code', '母父系統コード', None, '4', '9', '281', None],
        ['reserved', '予備', None, '6', 'X', '285', 'スペース'],
        ['newline', '改行', None, '2', 'X', '291', 'ＣＲ・ＬＦ']
    ]

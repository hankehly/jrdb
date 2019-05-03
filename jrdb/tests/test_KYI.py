import datetime
import os

from django.conf import settings
from django.forms import model_to_dict

from jrdb.models import choices, Program, Race, Contender, Horse, Trainer, Jockey
from jrdb.tests.base import JRDBTestCase
from jrdb.templates import KYI

TEMPLATE_PATH = os.path.join(settings.BASE_DIR, 'jrdb', 'tests', 'samples', 'KYI150801.txt')


class KYITestCase(JRDBTestCase):
    fixtures = ['racetrack', 'special_mention_code']

    @classmethod
    def setUpTestData(cls):
        t = KYI(TEMPLATE_PATH).extract()

        # only import the first row to make
        # test record easy to identify
        t.df = t.df.iloc[0].to_frame().T
        t.load()

        cls.program = Program.objects.first()
        cls.race = Race.objects.first()
        cls.horse = Horse.objects.first()
        cls.trainer = Trainer.objects.first()
        cls.jockey = Jockey.objects.first()
        cls.contender = Contender.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {'racetrack': 1, 'yr': 15, 'round': 1, 'day': '1'}
        self.assertSubDict(exp, act)

    def test_load_race(self):
        act = model_to_dict(self.race)
        exp = {'num': 1}
        self.assertSubDict(exp, act)

    def test_load_horse(self):
        act = model_to_dict(self.horse)
        exp = {
            'pedigree_reg_num': '13106308',
            'name': 'コスモベガス',
            'sex': choices.SEX.MALE,
            'owner_name': '岡田 繁幸氏',
            'owner_racetrack': 1,
            'symbol': choices.HORSE_SYMBOL.NA,
        }
        self.assertSubDict(exp, act)

    def test_load_trainer(self):
        act = model_to_dict(self.trainer)
        exp = {
            'name': '上原博之',
            'training_center_name': '美浦',
            'code': '10293'
        }
        self.assertSubDict(exp, act)

    def test_load_jockey(self):
        act = model_to_dict(self.jockey)
        exp = {
            'name': '黛弘人',
            'code': '10529',
        }
        self.assertSubDict(exp, act)

    def test_load_contender(self):
        act = model_to_dict(self.contender)
        exp = {
            'num': 1,
            'prel_idm': 27.0,
            'prel_jockey_idx': 0.8,
            'prel_info_idx': 0.1,
            'prel_total_idx': 27.9,
            'prel_run_style': choices.RUNNING_STYLE.OTP,
            'dist_apt': 0,
            'prel_improvement': choices.IMPROVEMENT.B,
            'rotation': 4,
            'odds_win_base': 15.7,
            'pop_win_base': 6,
            'odds_show': 3.4,
            'pop_show_base': 6,
            'sym_sp_c_dbl': 0,
            'sym_sp_c': 0,
            'sym_sp_t_dark': 0,
            'sym_sp_t': 8,
            'sym_sp_x': None,
            'sym_total_c_dbl': 2,
            'sym_total_c': 2,
            'sym_total_t_dark': 3,
            'sym_total_t': 73,
            'sym_total_x': None,
            'prel_pop_idx': 99,
            'prel_trainer_idx': -2.7,
            'prel_stable_idx': 3.6,
            'trainer_outlook': choices.TRAINER_HORSE_EVALUATION.NO_CHANGE,
            'stable_outlook': choices.STABLE_HORSE_EVALUATION.NO_CHANGE,
            'jockey_exp_1o2_place_rate': 14.2,
            'flat_out_run_idx': 97,
            'paddock_observed_hoof': '10',
            'yield_track_apt': choices.YIELDING_TRACK_APTITUDE.WEAK,
            'blinker': None,
            'mounted_weight': 540.0,
            'weight_reduction': None,
            'post_position': 1,
            'sym_overall': 6,
            'sym_idm': 6,
            'sym_info': 6,
            'sym_jockey': 6,
            'sym_stable': 6,
            'sym_trainer': 6,
            'is_flat_out_runner': True,
            'turf_apt': choices.APTITUDE_CODE.WEAK,
            'dirt_apt': None,
            'prel_b3f_time_idx': -14.3,
            'prel_pace_idx': -25.5,
            'prel_f3f_time_idx': -1.1,
            'prel_position_idx': -11.0,
            'prel_pace_cat': choices.PACE_CATEGORY.SLOW,
            'mid_race_position': 5,
            'mid_race_margin': 0.6,
            'mid_race_line': choices.RACE_LINE.INNER,
            'f3f_position': 6,
            'f3f_margin': 0.7,
            'f3f_race_line': choices.RACE_LINE.INNER,
            'goal_position': 4,
            'goal_margin': 0.8,
            'goal_race_line': choices.RACE_LINE.MIDDLE,
            'race_development_symbol': choices.RACE_DEVELOPMENT_SYMBOL.FAST_F3F,
            'dist_apt_2': None,
            'is_scratched': False,
            'flat_out_run_position': 8,
            'ls_idx_position': 4,
            'b3f_idx_position': 5,
            'pace_idx_position': 9,
            'f3f_idx_position': 3,
            'positioning_idx_position': 9,
            'jockey_exp_win_rate': 6.1,
            'jockey_exp_show_rate': 24.0,
            'transport_category': choices.TRANSPORT_CATEGORY.STAY,
            'figure_overall': None,
            'length_back': None,
            'length_body': None,
            'size_rump': None,
            'size_hindquarters': None,
            'size_belly': None,
            'size_head': None,
            'length_neck': None,
            'size_breast': None,
            'size_shoulder': None,
            'length_front': choices.FIGURE_LENGTH.NORMAL,
            'length_rear': choices.FIGURE_LENGTH.NORMAL,
            'stride_front': choices.FIGURE_STRIDE.NORMAL,
            'stride_rear': choices.FIGURE_STRIDE.NARROW,
            'length_pastern_front': None,
            'length_pastern_rear': None,
            'is_dock_raised': None,
            'tail_swing_intensity': None,
            'figure_sp_mention_1': None,
            'figure_sp_mention_2': None,
            'figure_sp_mention_3': None,
            'horse_sp_mention_1': None,
            'horse_sp_mention_2': None,
            'horse_sp_mention_3': None,
            'horse_start_idx': 0.0,
            'late_start_rate': 0.0,
            'big_bet_idx': 41,
            'sym_big_bet': 3,
            'rank_lowered': choices.RANK_LOWERED.NO_CHANGE,
            'flat_out_run_type': choices.FLAT_OUT_RUN_TYPE.A3,
            'rest_reason': None,
            'prior_context_surface': choices.PRIOR_CONTEXT_SURFACE.NO_CHANGE,
            'is_longest_race_dist_yet': True,
            'prior_context_race_class': choices.PRIOR_CONTEXT_RACE_CLASS.NO_CHANGE,
            'nth_race_since_stable_change': 0,
            'nth_race_since_castration': 0,
            'nth_race_since_training_start': 1,
            'training_start_date': datetime.date(2015, 7, 18),
            'nth_day_since_training_start': 14,
            'pasture_name': 'コスモヴューファーム',
            'pasture_rank': choices.PASTURE_RANK.C,
            'stable_rank': choices.STABLE_RANK.NORMAL
        }

        self.assertSubDict(exp, act)

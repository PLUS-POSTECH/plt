import os
import binascii
import re
from datetime import datetime

from django.apps import AppConfig
from django.contrib.auth import get_user_model

from .models import XssLog

Team = get_user_model()

class XssConfig(AppConfig):
    name = 'xss'


def prepare_xss(target_team_name: str, query: str):
    target_team_list = Team.objects.filter(username=target_team_name)

    if len(target_team_list) != 1:
        return False, None
    
    target_team = target_team_list[0]

    ok, msg = is_valid_query(target_team, query)
    if not ok:
        return False, msg

    return True, target_team.xss_filter.csp_rule_list



def is_valid_query(target_team: Team, query: str):

    if len(Team.objects.filter(username=target_team.username)) == 0:
        return False, "그런 이름을 가진 팀은 이 마을에 없다냥"
    
    max_len = target_team.xss_filter.max_len

    if max_len < len(query):
        return False, "말을 좀 짧게 하라냥!"

    regex_filter_list = target_team.xss_filter.regex_rule_list.all()

    for r in regex_filter_list:
        p = re.compile(r.regexp)
        if p.match(query):
            return False, "그런 단어는 쓰지 말아달라냥.."

    return True, ""


def get_time_passed_after_last_attack(attack_team, target_team):
    last_attack_time = 0
    try:
        last_attack = XssLog.objects.filter(from_team=attack_team,
                                            to_team=target_team,
                                            succeed=True).latest()
        last_attack_time = int(last_attack.created_at.strftime("%Y%m%d%H%M%S"))
    except XssLog.DoesNotExist:
        pass
    
    return int(datetime.now().strftime("%Y%m%d%H%M%S")) - last_attack_time


def attack_xss(attack_team, target_team, query, csp):
    hash = str(binascii.hexlify(os.urandom(32)),'utf8')
    xss_log = XssLog.objects.create(hash=hash)
    xss_log.from_team = attack_team
    xss_log.to_team = target_team
    xss_log.csp.add(*csp.all())
    xss_log.query = query
    xss_log.save()

    return xss_log
    
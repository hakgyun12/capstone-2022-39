import requests
import json
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


def validator(value):
    SERVICE_KEY = ""
    url = f"https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey={SERVICE_KEY}&returnType=JSON"

    company_no = "3128105829"

    headers = {
        "Content-Type": "application/json"
    }

    json_body = {
        "b_no": [
            company_no
        ]
    }

    res = requests.post(url, headers=headers, data=json.dumps(json_body))
    dic_res = json.loads(res.text)
    get_status = dic_res['data'][0]['b_stt']

    if '계속사업자' in get_status:
        return True
    else:
        return False


def validate_company_id(value):
    if validator(value) is True:
        return value
    else:
        raise ValidationError("잘못된 사업자 등록번호 입니다.")

class User(AbstractUser):
    website_url = models.URLField(blank=True)
    company_id = models.CharField(blank=True, max_length=12, validators=[validate_company_id])

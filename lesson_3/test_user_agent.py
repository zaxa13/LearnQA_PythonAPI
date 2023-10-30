import requests
import pytest
import json

users_agents_values = [
    ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; '
     'Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
    ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 '
     '(KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'),
    ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html'),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
     '(KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'),
    ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
     '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')]

expected_values = [
    ({'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
    ({'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
    ({'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
    ({'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
    ({'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})]

data_list = list(zip(users_agents_values, expected_values))


class TestUserAgent:
    @pytest.mark.parametrize('user_agent_val, expected', data_list)
    def test_user_agent(self,user_agent_val, expected):
        payload = {"User-Agent": user_agent_val}
        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers=payload)
        assert response.status_code == 200, "Response code is not 200"
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"


    # assert "User-Agent" in response.json(), "The 'User-Agent' is not in the response"
        assert expected["platform"] == response_as_dict["platform"], "Value in field 'platform' not equal by 'User-Agent'"
        assert expected["browser"] == response_as_dict["browser"], "Value in field 'browser' not equal by 'User-Agent'"
        assert expected["device"] == response_as_dict["device"], "Value in field 'device' not equal by 'User-Agent'"
import index
import unittest
from moto import mock_dynamodb2
import boto3
import pytest

    
# when textScrubber is called, people tagged with @ will be removed
def test_textScrubber_remove_at_mention():
    text = '@TestPerson check this out!'
    
    assert index.textScrubber(text) == 'check this out!'
    
# when textScrubber is called, # will be removed 
def test_textScrubber_remove_hashtag():
    text = '@TestPerson check this out! #thisisneat #wow'
    
    assert index.textScrubber(text) == 'check this out! thisisneat wow'
    
# when textScrubber is called, Retweets with RT will be removed
def test_textScrubber_remove_Retweet():
    text = 'RT@TestPerson check this out! #thisisneat #wow'
    
    assert index.textScrubber(text) == 'check this out! thisisneat wow'
    
# when textScrubber is called, any hyperlinks are removed
def test_textScrubber_remove_hyperlink():
    text = 'RT@TestPerson check this out! #thisisneat #wow https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    
    assert index.textScrubber(text) == 'check this out! thisisneat wow'
    
# when a payload is sent to the lambda_handler, it processes the payload (single tweet test)
def test_lambda_handler():
    # dummy event
    event = {
        "Records": [{
           'body': "{\n  \"Type\": \"Notification\",\n  \"MessageId\": \"dc1e94d9-56c5-5e96-808d-cc7f68faa162\",\n  \"TopicArn\": \"arn:aws:sns:us-east-2:111122223333:ExampleTopic1\",\n  \"Subject\": \"TestSubject\",\n  \"Message\": \"{'created_at': 'Tue Apr 19 13:01:45 +0000 2022', \\n         'id': 1516401667842920449, \\n         'id_str': '1516401667842920449', \\n         'text': 'RT @JerseyRizzo: RT if you want Elon Musk to reinstate TRUMP on Twitter!', \\n         'truncated': False, \\n         'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [{'screen_name': 'JerseyRizzo', 'name': 'Phil Rizzo 🇺🇸', 'id': 373364557, 'id_str': '373364557', 'indices': [3, 15]}], 'urls': []}, \\n         'metadata': {'iso_language_code': 'en', 'result_type': 'recent'}, \\n         'source': '<a href=\\\"http://twitter.com/download/android\\\" rel=\\\"nofollow\\\">Twitter for Android</a>', \\n         'in_reply_to_status_id': None, \\n         'in_reply_to_status_id_str': None, \\n         'in_reply_to_user_id': None, \\n         'in_reply_to_user_id_str': None, \\n         'in_reply_to_screen_name': None, \\n         'user': {'id': 1481362322396438536, \\n                  'id_str': '1481362322396438536', \\n                  'name': 'Yolanda Matos', \\n                  'screen_name': 'Yolanda38767841', \\n                  'location': '', \\n                  'description': 'Veterana', \\n                  'url': None, \\n                  'entities': {'description': {'urls': []}}, \\n                  'protected': False, 'followers_count': 163, \\n                  'friends_count': 596, \\n                  'listed_count': 5, \\n                  'created_at': 'Wed Jan 12 20:29:31 +0000 2022', \\n                  'favourites_count': 4105, \\n                  'utc_offset': None, \\n                  'time_zone': None, \\n                  'geo_enabled': False, \\n                  'verified': False, \\n                  'statuses_count': 561, \\n                  'lang': None, \\n                  'contributors_enabled': False, \\n                  'is_translator': False, \\n                  'is_translation_enabled': False, \\n                  'profile_background_color': 'F5F8FA', \\n                  'profile_background_image_url': None, \\n                  'profile_background_image_url_https': None, \\n                  'profile_background_tile': False, \\n                  'profile_image_url': 'http://pbs.twimg.com/profile_images/1481362728547667968/HxMcPuNQ_normal.png', \\n                  'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1481362728547667968/HxMcPuNQ_normal.png', \\n                  'profile_link_color': '1DA1F2', \\n                  'profile_sidebar_border_color': 'C0DEED', \\n                  'profile_sidebar_fill_color': 'DDEEF6', \\n                  'profile_text_color': '333333', \\n                  'profile_use_background_image': True, \\n                  'has_extended_profile': True, \\n                  'default_profile': True, \\n                  'default_profile_image': False, 'following': False, \\n                  'follow_request_sent': False, 'notifications': False, \\n                  'translator_type': 'none', \\n                  'withheld_in_countries': []},\\n         'geo': None, 'coordinates': None, \\n         'place': None, 'contributors': None, \\n         'retweeted_status': {'created_at': 'Mon Apr 18 13:58:00 +0000 2022',\\n                              'id': 1516053434201350148,\\n                              'id_str': '1516053434201350148',\\n                              'text': 'RT if you want Elon Musk to reinstate TRUMP on Twitter!',\\n                              'truncated': False,\\n                              'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [], 'urls': []},\\n                              'metadata': {'iso_language_code': 'en', 'result_type': 'recent'},\\n                              'source': '<a href=\\\"https://mobile.twitter.com\\\" rel=\\\"nofollow\\\">Twitter Web App</a>',\\n                              'in_reply_to_status_id': None,\\n                              'in_reply_to_status_id_str': None,\\n                              'in_reply_to_user_id': None,\\n                              'in_reply_to_user_id_str': None,\\n                              'in_reply_to_screen_name': None, \\n                              'user': {'id': 373364557,\\n                                       'id_str': '373364557',\\n                                       'name': 'Phil Rizzo 🇺🇸',\\n                                       'screen_name': 'JerseyRizzo', \\n                                       'location': 'New Jersey', \\n                                       'description': \\\"Husband • Father • Pastor • Businessman • Freedom Fighter • Candidate for New Jersey's 7th Congressional District • #RizzoMania\\\",\\n                                       'url': 'https://t.co/Gyb5RruZQW',\\n                                       'entities': {'url': {'urls': [{'url': 'https://t.co/Gyb5RruZQW', 'expanded_url': 'https://www.jerseyrizzo.com/', 'display_url': 'jerseyrizzo.com', 'indices': [0, 23]}]},\\n                                                    'description': {'urls': []}},\\n                                       'protected': False,\\n                                       'followers_count': 13460, \\n                                       'friends_count': 2002, \\n                                       'listed_count': 52, \\n                                       'created_at': 'Wed Sep 14 13:08:33 +0000 2011',\\n                                       'favourites_count': 10373, \\n                                       'utc_offset': None, \\n                                       'time_zone': None, \\n                                       'geo_enabled': True, \\n                                       'verified': True,\\n                                       'statuses_count': 9601,\\n                                       'lang': None, \\n                                       'contributors_enabled': False, \\n                                       'is_translator': False, \\n                                       'is_translation_enabled': False, \\n                                       'profile_background_color': 'C0DEED', \\n                                       'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', \\n                                       'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', \\n                                       'profile_background_tile': False, \\n                                       'profile_image_url': 'http://pbs.twimg.com/profile_images/1352472434558062594/tHbIWcZo_normal.jpg', \\n                                       'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1352472434558062594/tHbIWcZo_normal.jpg', \\n                                       'profile_banner_url': 'https://pbs.twimg.com/profile_banners/373364557/1623290959', \\n                                       'profile_link_color': 'FF691F', \\n                                       'profile_sidebar_border_color': '000000', \\n                                       'profile_sidebar_fill_color': 'DDEEF6', \\n                                       'profile_text_color': '333333', \\n                                       'profile_use_background_image': True, \\n                                       'has_extended_profile': False, \\n                                       'default_profile': False, \\n                                       'default_profile_image': False, \\n                                       'following': False, \\n                                       'follow_request_sent': False, \\n                                       'notifications': False, \\n                                       'translator_type': 'none', \\n                                       'withheld_in_countries': []}, \\n                              'geo': None,\\n                              'coordinates': None,\\n                              'place': None, \\n                              'contributors': None,\\n                              'is_quote_status': False,\\n                              'retweet_count': 6967,\\n                              'favorite_count': 16736,\\n                              'favorited': False, \\n                              'retweeted': False, \\n                              'lang': 'en'}, \\n         'is_quote_status': False,\\n         'retweet_count': 6967,\\n         'favorite_count': 0,\\n         'favorited': False,\\n         'retweeted': False, \\n         'lang': 'en'}\",\n  \"Timestamp\": \"2021-02-16T21:41:19.978Z\",\n  \"SignatureVersion\": \"1\",\n  \"Signature\": \"FMG5tlZhJNHLHUXvZgtZzlk24FzVa7oX0T4P03neeXw8ZEXZx6z35j2FOTuNYShn2h0bKNC/zLTnMyIxEzmi2X1shOBWsJHkrW2xkR58ABZF+4uWHEE73yDVR4SyYAikP9jstZzDRm+bcVs8+T0yaLiEGLrIIIL4esi1llhIkgErCuy5btPcWXBdio2fpCRD5x9oR6gmE/rd5O7lX1c1uvnv4r1Lkk4pqP2/iUfxFZva1xLSRvgyfm6D9hNklVyPfy+7TalMD0lzmJuOrExtnSIbZew3foxgx8GT+lbZkLd0ZdtdRJlIyPRP44eyq78sU0Eo/LsDr0Iak4ZDpg8dXg==\",\n  \"SigningCertURL\": \"https://sns.us-east-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem\",\n  \"UnsubscribeURL\": \"https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:111122223333:ExampleTopic1:e1039402-24e7-40a3-a0d4-797da162b297\"\n}" 
        }]
    }
    
    # mock dynamoDB client (look up how to test post request)
    
    # compare mock to actual
    
    context = " "
    response = 200
    actual = index.lambda_handler(event, context)['ResponseMetadata']['HTTPStatusCode']
    assert  actual == response
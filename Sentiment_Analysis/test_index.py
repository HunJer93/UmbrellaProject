import index
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
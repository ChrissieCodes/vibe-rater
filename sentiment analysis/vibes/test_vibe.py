# TODO:a shell script test.sh that includes that and chmod u+x then do ./test.sh so you don't have to write it out every time
from vibes import vibe

username = 'chrissiecodes'
good_vibes = [0.4, 0.5, 0.39]
neg_vibes = [0.2, 0.2, 0.2, 0.25]

def test_store_vibes():
    username = 'chrissiecodes'
    positive_score = 0.60
    negative_score = 0.20
    data = vibe.example_data(username, good_vibes, neg_vibes)
    vibe.vibe_rater_store(username, positive_score, negative_score, data)
    assert good_vibes == [0.4, 0.5, 0.39, 0.60]
    assert neg_vibes == [0.2, 0.2, 0.2, 0.25, 0.2]
    

    
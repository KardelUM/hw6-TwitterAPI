#########################################
##### Name: Yufeng Chen             #####
##### Uniqname: Kardel              #####
#########################################
from hw6_twitter_starter_code import *


def find_most_common_cooccurring_hashtag2(tweet_data, hashtags_to_ignore):
    ''' Finds the hashtag that most commonly co-occurs with the hashtag
    queried in make_request_with_cache().

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query
    hashtags_to_ignore: list
        the same hashtag that is queried in make_request_with_cache()
        (e.g. "#MarchMadness2021")

    Returns
    -------
    string
        the hashtag that most commonly co-occurs with the hashtag
        queried in make_request_with_cache()

    '''
    hashtag_count = dict()
    if "statuses" not in tweet_data:
        return ""
    hashtags_to_ignore = [hashtag_to_ignore.replace("#", "").replace("%23", "").lower() for hashtag_to_ignore in
                          hashtags_to_ignore]
    for status in tweet_data["statuses"]:

        hashtags = [hashtag['text'].lower() for hashtag in status['entities']['hashtags'] if
                    hashtag["text"].lower() not in hashtags_to_ignore]
        for hashtag in hashtags:
            if hashtag not in hashtag_count:
                hashtag_count[hashtag] = 1
            else:
                hashtag_count[hashtag] += 1
    ''' Hint: In case you're confused about the hashtag_to_ignore 
    parameter, we want to ignore the hashtag we queried because it would 
    definitely be the most occurring hashtag, and we're trying to find 
    the most commonly co-occurring hashtag with the one we queried (so 
    we're essentially looking for the second most commonly occurring 
    hashtags).'''
    return max(hashtag_count, key=hashtag_count.get)


def find10keywords(tweetdata):
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    sw_url = "http://xpo6.com/wp-content/uploads/2015/01/stop-word-list.txt"
    req = urllib.request.Request(sw_url, headers=headers)
    response = urllib.request.urlopen(req)
    r = response.read()
    response.close()
    swlist_r = r.decode("UTF-8")
    sw_list = swlist_r.strip().split("\r\n")
    URL_PATTERN = "^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$"
    d = {}
    import re
    for status in tweetdata["statuses"]:
        s = status['text']
        if "#" in s:
            # remove hashtags
            s = re.sub("#\w+", "", s)
        if "'" in s:
            # remove abbreviation
            # Since 's->"is"/"has" 'd -> "would" are all stop words, we can just remove them
            s = re.sub("'\w+", "", s)
        if "http" in s:
            # remove links
            s = re.sub("(https|http)://t.co/\w+", "", s)
        res = re.findall(r'\w+', s)
        for word in res:
            word = word.lower()
            if word in sw_list or word == "rt":
                # stopword, ignore
                pass
            else:
                if word in d:
                    d[word] += 1
                else:
                    d[word] = 1
    return sorted(d, key=d.get, reverse=True)[:10]


def main():
    CACHE_DICT = open_cache()
    baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    count = 100
    while True:
        token = input("please input the hashtag, I will show the most commonly co-occurring hashtag with that: ")
        # token = "2020election"
        if token == "exit":
            save_cache(CACHE_DICT)
            return
        if token[0] != "#":
            hashtag = "#" + token
        else:
            hashtag = token
        tweet_data = make_request_with_cache(baseurl, hashtag, count)
        ignoring_hashtags = [hashtag]
        for _ in range(3):
            most_common_cooccurring_hashtag = find_most_common_cooccurring_hashtag2(tweet_data, ignoring_hashtags)
            ignoring_hashtags.append(most_common_cooccurring_hashtag)
        print("The top 3 most commonly co-occurring hashtag with {} is {},{} and {}.".format(ignoring_hashtags[0],
                                                                                           ignoring_hashtags[1],
                                                                                           ignoring_hashtags[2],
                                                                                           ignoring_hashtags[3]))
        keywords = find10keywords(tweet_data)
        s = ""
        for keyword in keywords:
            s += keyword + ", "
        s = s[:-2]
        print("The top 10 most commonly co-occurring words are:", s)
        print()



if __name__ == '__main__':
    main()

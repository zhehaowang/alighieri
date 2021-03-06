#!/usr/bin/env python3

"""
Limbo (the first layer of inferno) looks for profiles in a given glob and builds an alternative view to CMB app
"""

import argparse
import os
import glob
import json
from uuid import UUID

def parse_args():
    parser = argparse.ArgumentParser("""
        Looks for profiles in a given directory and builds an alternative static html view to CMB app.
        example usage:
          ./limbo.py --glob ../examples/*.json
    """)
    parser.add_argument("--glob", help="the profile files (json) glob", default="../data/*.json")
    parser.add_argument("--mode", help="the mode to use [hist|token|html]", default="html")
    args = parser.parse_args()
    return args

class ProfileExtractor():
    def __init__(self):
        self.profiles = {}
        return

    def _try_extract(self, o):
        def _try_field_default(obj, field, default):
            return obj[field] if field in obj and obj[field] is not None else default
        
        def _extract_photos(obj):
            return [entry["iphone_fullscreen"] for entry in obj]

        for entry in o:
            if "profile" in entry:
                profile = entry["profile"]
                profile_id = profile["id"]
                if profile_id not in self.profiles and "profile" in entry:
                    self.profiles[profile_id] = {
                        "age": int(_try_field_default(profile, "age", -1)),
                        "height_cm": int(_try_field_default(profile, "height_cm", -1)),

                        "degree": _try_field_default(profile, "degree", []),
                        "education": _try_field_default(profile, "education", []),
                        "ethnicity": _try_field_default(profile, "ethnicity", ""),
                        "religion": _try_field_default(profile, "religion", ""),
                        "occupation": _try_field_default(profile, "occupation", ""),
                        "employer": _try_field_default(profile, "employer", ""),
                        "name": _try_field_default(profile, "user__first_name", ""),

                        "interested_in": _try_field_default(profile, "interested_in", ""),
                        "i_am": _try_field_default(profile, "i_am", ""),
                        "appreciate_in_date": _try_field_default(profile, "appreciate_in_date", ""),
                        "photos": _extract_photos(profile["photos"]),

                        "likes": int(_try_field_default(entry, "rising_bagel_count", -1))
                    }
        return
    
    def extract_profile(self, json_in):
        if isinstance(json_in, list):
            self._try_extract(json_in)
        elif "results" in json_in:
            self._try_extract(json_in["results"])
        return

def main():
    args = parse_args()

    pe = ProfileExtractor()
    files = glob.glob(args.glob)
    for f in files:
        with open(f, 'r') as infile:
            try:
                pe.extract_profile(json.loads(infile.read()))
            except json.JSONDecodeError as e:
                print(e)
    
    print("retrieved {} unique profiles".format(len(pe.profiles)))

    sorted_profiles = sorted(pe.profiles.values(), key=lambda x: x["likes"])

    if args.mode == "hist":
        gen_plot(sorted_profiles)
    elif args.mode == "token":
        gen_token(sorted_profiles)
    elif args.mode == "html":
        gen_html(sorted_profiles)
    else:
        raise NotImplementedError("{} is not implemented".format(args.mode))

    return

def gen_plot(profiles):
    """plot histogram of likes
    """
    for p in sorted_profiles:
        print(p["name"], p["likes"])
    
    plot_hist([p["likes"] for p in profiles if p["likes"] >= 0])
    return
    
def gen_token(profiles):
    # nouns and adjectives
    appreciate = tokenize([p["appreciate_in_date"] for p in profiles], ['JJ', 'NN', 'NNP', 'NNS'])
    i_am = tokenize([p["i_am"] for p in profiles], ['JJ', 'NN', 'NNP', 'NNS'])
    # nouns and verbs
    interest = tokenize([p["interested_in"] for p in profiles], ['V', 'NN', 'NNP', 'NNS'])
    
    print("most commonly sought after: {}".format(appreciate))
    print("most common attributes: {}".format(i_am))
    print("most common interests: {}".format(interest))
    return

def gen_html(profiles):
    return

# post processing funcs.
# for now just plot histagram of likes. to be moved once we flesh out what stats we want
def plot_hist(series):
    import numpy as np
    import matplotlib.pyplot as plt
    series_in = np.array(series)
    binwidth = 20

    print("Average number of likes: {}".format(np.mean(series_in)))
    print("Std: {}".format(np.std(series_in)))

    plt.title("Distribution of number of likes profiles")
    plt.xlabel('Number of likes')
    plt.ylabel('Number of profiles')

    plt.hist(series_in, bins=range(min(series_in), max(series_in) + binwidth, binwidth))
    plt.show()

def tokenize(series, filter_category):
    import nltk

    # from nltk.stem.snowball import SnowballStemmer
    # stemmer = SnowballStemmer("english")
    # print(stemmer.stem(t))
    
    from nltk.corpus import stopwords
    from nltk.corpus import brown

    word_count = {}

    for s in series:
        tokens = nltk.word_tokenize(s)
        filtered_words = [word for word in tokens if word not in stopwords.words('english') and word.isalpha()]
        
        # brown_tagged = brown.tagged_words(tagset='universal')
        # word_tag_pairs = nltk.bigrams(brown_tagged)
        # noun_preceders = [a[1] for (a, b) in word_tag_pairs if b[1] == 'NOUN']
        # fdist = nltk.FreqDist(noun_preceders)
        # print([tag for (tag, _) in fdist.most_common()])
        
        in_this = {}
        pos_tag = nltk.pos_tag(filtered_words)
        for w in pos_tag:
            if w[1] in filter_category:
                sanitized = w[0].lower()
                if sanitized in in_this:
                    continue
                in_this[sanitized] = True
                if sanitized in word_count:
                    word_count[sanitized] += 1
                else:
                    word_count[sanitized] = 1
        # print(filtered_words)
    
    word_count_sorted = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return word_count_sorted[:10]

def gen_html():


if __name__ == "__main__":
    main()

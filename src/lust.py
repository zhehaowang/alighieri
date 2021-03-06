#!/usr/bin/env python3

"""
Lust (the second layer of inferno) looks as far back as it can for profiles in a given session id's queue.
"""

import argparse
import os
import json
import requests
import time

def parse_args():
    parser = argparse.ArgumentParser("""
        Looks for profiles in a given directory and builds an alternative static html view to CMB app.
        example usage:
          ./limbo.py --session s --save_pics
    """)
    parser.add_argument("--session", help="the session cookie to use", required=True)
    parser.add_argument("--save_pics", help="if this should save pics to local", action="store_true")
    parser.add_argument("--outdir", help="json outdir", default="../data/")
    args = parser.parse_args()
    return args


HEADERS = {
    "accept": "application/json",
    "appstore-version": "6.27.0",
    "app-version": "8583",
    "accept-language": "en",
    "user-agent": "CMB/6.27.0 (com.coffeemeetsbagel.mobile.ios; build:8583; iOS 12.1.4) Alamofire/4.8.0"
}


class Requester():
    def __init__(self, session, outdir):
        self._headers = HEADERS
        self._cookies = {
            "sessionid": session
        }
        self._outdir = outdir
        self.api_endpoint = "https://api.coffeemeetsbagel.com/bagels"
        return

    def send_request(self, before=None):
        url = "{}?embed=profile".format(self.api_endpoint)
        
        params = {"embed": "profile"}
        if before:
            params["cursor_before"] = before
        response = requests.get(url, params, headers=self._headers, cookies=self._cookies)
        print("retrieved {}".format(response.url))

        if response.status_code != 200:
            print("error response {}".format(response.status_code))
        else:
            if not before:
                ts = int(time.time())
            else:
                ts = before
            outfile_name = os.path.join(self._outdir, "out_{}.json".format(ts))
            with open(outfile_name, "w") as outfile:
                outfile.write(response.text)
            print("written {}".format(outfile_name))
            
            response_obj = json.loads(response.text)

            # assume we start from the latest, which seems fair
            if "more_before" in response_obj and response_obj["more_before"]:
                cursor_before = response_obj["cursor_before"]
                self.send_request(cursor_before)
        return

    def run(self):
        self.send_request()
        return

class Searcher():
    def __init__(self, session, outdir):
        self._headers = HEADERS
        self._outdir = outdir
        self._cookies = {
            "sessionid": session
        }
        self.api_endpoint = "https://api.coffeemeetsbagel.com/discoversearch"

        self.criteria = {
            "age_from": range(22, 28),
            "degree": ["bachelors", "phd", "masters"],
            "ethnicity": ["Asian"],
            "height_cm_from": range(120, 190, 5),
            "max_distance_km": [16],
            "recently_active": ["true"]
        }
        return

    def _permutate(self):
        result_params = []
        current = {}
        keys = list(self.criteria.keys())
        keyidx = 0

        def _append(keyidx, current):
            if keyidx == len(keys):
                result_params.append(dict(current))
                return
            for v in self.criteria[keys[keyidx]]:
                current[keys[keyidx]] = v
                _append(keyidx + 1, current)
        
        _append(keyidx, current)
        return result_params

    def _query(self):
        return
    
    def run(self):
        params = self._permutate()
        url = "{}?embed=profile".format(self.api_endpoint)
        for param_set in params:
            # a most unfortunate hack
            param_set["height_cm_to"] = param_set["height_cm_from"] + 5
            
            response = requests.get(url, param_set, headers=self._headers, cookies=self._cookies)
            if response.status_code != 200:
                print("error response {}".format(response.status_code))
            else:
                ts = int(time.time())
                outfile_name = os.path.join(self._outdir, "search_{}_{}.json".format(param_set, ts))
                with open(outfile_name, "w") as outfile:
                    outfile.write(response.text)
                print("written {}".format(outfile_name))
        
        return

def main():
    args = parse_args()

    if args.save_pics:
        raise NotImplementedError("save_pics is not implemented")

    # requester = Requester(args.session, args.outdir)
    # requester.run()

    searcher = Searcher(args.session, args.outdir)
    searcher.run()
    return

if __name__ == "__main__":
    main()

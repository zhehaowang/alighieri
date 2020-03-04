# Alighieri

This is supposed to be guided through heaven by a certain Beatrice?

"Dante claims to have met a 'Beatrice' only twice, on occasions separated by nine years, but was so affected by the meetings that he carried his love for her throughout his life."

Lol Dante.

### Scratching

* `rising_bagel_count` positively correlated with matches / mmr
* `photo_score` with face detection. Presumably those with one and only one face score highest
* protocol
  * Although the app's request has "ProfileID" and "Authorization" in http header, the only field that decides what results we get back seems to be the "sessionid" in Cookies. The backend uses this to identify you and your queue.
  * `/bagels`, Suggestions tab
    * `embed=profile`: pull in the user profile in the response.
    * `prefetch=true`: with this it pulled 22 profiles, without it pulled 50 seems to be a mesh of today's and yesterday's. This is presumably the option that limits your daily number.
    * `cursor_before=seconds_since_epoch`: with this it pulled 50 with matching timestamp. One possibility is them having a backend batch processing job populating a queue of suggestions for you, and the app queries for a number of such everyday. So far nothing seems to be stopping us from going back in time. 50 seems to be the default page size. `more_before` and `more_after` are presumably pagination indicators.
    * `couples_only=true`: pull only the ones you've matched with.
    * `id=cc9ec7bd-486b-32e3-ba52-c4a978bc302e`: pull in the particular profile. The RFC 4122 GUID matches with the one returned in results `"id"` field. Not sure if this can pull profiles not in your queue. Should try with my own GUID.
    * The `last_updated` field could be when the queue last interacted with this profile? There seems to be a batch job running at 5pm, e.g.
    * birthdays are almost certainly always wrong.
    * pics can be accessed without a token on cloudfront (presumably only for caching, as CDN?). Url pattern would probably be hard to infer.
    * `pair_bagel_type=0` seems to be the ones you liked (but did not like + comment?), `=-1` seems to be the one you passed.
    * `pair_action=1` seems to be the ones I matched with. No idea what 0 or 2 means.
    * `action=[0-9]+` seems related with how many times this profile is represented to you / opened?
    * `source` seen recommendation and boost_v1.0
  * `/givetakes`, Discover tab
    * Notably they don't have `rising_bagel_count` and the request got back 20, a few more than the daily discover count.
    * `updated_after=seconds_since_epoch` param

* Possibilities:
  * Free interaction with your queue: history of matches, upcoming matches, and can potentially see more bagels without spending beans. (Then with enough number of fake accounts, we can sample the population.)

Firebase, XMPP chat, send chat message, like in suggestion, like with msg, like in discover, those who like you?

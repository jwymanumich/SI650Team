import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { strictEqual } from 'assert';
import { Observable } from 'rxjs';

@Injectable()
export class TwitterTopicService {
    constructor(private http: HttpClient) { }

    configUrl = 'assets/config.json';
    twittertopicurl(name, count) {
        var str = `http://127.0.0.1:5000/twittername/${name}/topics/${count}?force_call=true`;
        return str;
    }

    twittertoptweetsurl(name, count) {
        var str = `http://127.0.0.1:5000/twittername/${name}/top_tweets/${count}?force_call=true`;
        return str;
    }

    twittertoptweetsldaurl(name, count) {
        var str = `http://127.0.0.1:5000/twittername/${name}/top_tweets_lda/${count}?force_call=true`;
        return str;
    }

    twittertoptweetsrandomurl(name, count) {
        var str = `http://127.0.0.1:5000/twittername/${name}/top_tweets_random/${count}?force_call=true`;
        return str;
    }

    getTwitterTopics(handle): Observable<any[]> {
        var url = this.twittertopicurl(handle, '10')
        return this.http.get<any[]>(url);
    }

    getTwitterTopTweets(handle): Observable<Tweet[]> {
        var url = this.twittertoptweetsurl(handle, '10')
        return this.http.get<Tweet[]>(url);
    }

    getTwitterTopTweetsLda(handle): Observable<Tweet[]> {
        var url = this.twittertoptweetsldaurl(handle, '10')
        return this.http.get<Tweet[]>(url);
    }

    getTwitterTopTweetsRandom(handle): Observable<Tweet[]> {
        var url = this.twittertoptweetsrandomurl(handle, '10')
        return this.http.get<Tweet[]>(url);
    }
}


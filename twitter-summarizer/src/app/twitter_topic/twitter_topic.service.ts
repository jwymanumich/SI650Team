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

    getTwitterTopics(handle): Observable<Tweet[]> {
        console.log("getTwitterTopics")
        var url = this.twittertopicurl(handle, '10')
        console.log(url)
        return this.http.get<Tweet[]>(url);
    }

    getTwitterTopTweets(handle): Observable<Tweet[]> {
        console.log("getTwitterTopTweets")
        var url = this.twittertoptweetsurl(handle, '10')
        console.log(url)
        return this.http.get<Tweet[]>(url);
    }
}


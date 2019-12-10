import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { strictEqual } from 'assert';

@Injectable()
export class TwitterTopicService {
    constructor(private http: HttpClient) { }

    configUrl = 'assets/config.json';
    twittertopicurl(name, count) {
        var str = `http://127.0.0.1:5000/twittername/${name}/topics/${count}`;
        return str;
    } 

    twittertoptweetsurl(name, count) {
        var str = `http://127.0.0.1:5000/twittername/${name}/top_tweets/${count}`;
        return str;
    } 

    getTwitterTopics(handle) {
        console.log("getTwitterTopics")
        var url = this.twittertopicurl(handle, '10')
        console.log(url)

        var headers = new HttpHeaders();
        headers = headers.set('Access-Control-Allow-Origin', '*');
        const httpOptions = {
            headers: new HttpHeaders({
              'Access-Control-Allow-Origin':  '*'
            })
          }; 
        return this.http.get(url, httpOptions);
    }

    getTwitterTopTweets(handle) {
        console.log("getTwitterTopTweets")
        var url = this.twittertoptweetsurl(handle, '10')
        console.log(url)

        var headers = new HttpHeaders();
        headers = headers.set('Access-Control-Allow-Origin', '*');
        const httpOptions = {
            headers: new HttpHeaders({
              'Access-Control-Allow-Origin':  '*'
            })
          }; 
        return this.http.get(url, httpOptions);
    }
}


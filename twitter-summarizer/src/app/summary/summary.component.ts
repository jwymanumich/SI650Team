import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TwitterTopicService } from '../twitter_topic/twitter_topic.service';

@Component({
  selector: 'app-summary',
  templateUrl: './summary.component.html',
  styleUrls: ['./summary.component.css']
})
export class SummaryComponent implements OnInit {

  public handle: string;

  public tweets: string[];

  constructor(private route: ActivatedRoute,
    private twitterService: TwitterTopicService) { }

  ngOnInit() {
    this.handle = this.route.snapshot.paramMap.get('id');
    this.getSummary();
  }

  getSummary() {
    this.twitterService.getTwitterTopTweets(this.handle.replace('@', '')).subscribe(result => {
      this.tweets = [];
      result.forEach(tweet => {
        this.tweets.push(tweet.id);
      })
    });
  }
}

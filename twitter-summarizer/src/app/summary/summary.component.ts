import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NgxSpinnerService } from "ngx-spinner";
import { TwitterTopicService } from '../twitter_topic/twitter_topic.service';

@Component({
  selector: 'app-summary',
  templateUrl: './summary.component.html',
  styleUrls: ['./summary.component.css']
})
export class SummaryComponent implements OnInit {

  public handle: string;

  public lexTweets: string[];
  public ldaTweets: string[];
  public ranTweets: string[];

  constructor(private route: ActivatedRoute,
    private twitterService: TwitterTopicService,
    private spinner: NgxSpinnerService) { }

  ngOnInit() {
    this.handle = this.route.snapshot.paramMap.get('id');
    this.getLexSummary();
  }

  tabClick(tab) {
    const idx = tab.index;
    if(idx == 0) { // LexRank
      this.getLexSummary();
    } else if(idx == 1) { // LatentDirichletAllocation
      this.getLdaSummary();
    } else { // Random
      this.getRanSummary();
    }
  }

  getLexSummary() {
    if(this.lexTweets) return;
    this.spinner.show();
    this.twitterService.getTwitterTopTweets(this.handle.replace('@', '')).subscribe(result => {
      this.lexTweets = [];
      result.forEach(tweet => {
        this.lexTweets.push(tweet.id);
      })
      this.spinner.hide();
    });
  }

  getLdaSummary() {
    if(this.ldaTweets) return;
    this.spinner.show();
    this.twitterService.getTwitterTopTweetsLda(this.handle.replace('@', '')).subscribe(result => {
      this.ldaTweets = [];
      result.forEach(tweet => {
        this.ldaTweets.push(tweet.id);
      })
      this.spinner.hide();
    });
  }

  getRanSummary() {
    if(this.ranTweets) return;
    this.spinner.show();
    this.twitterService.getTwitterTopTweetsRandom(this.handle.replace('@', '')).subscribe(result => {
      this.ranTweets = [];
      result.forEach(tweet => {
        this.ranTweets.push(tweet.id);
      })
      this.spinner.hide();
    })
  }
}

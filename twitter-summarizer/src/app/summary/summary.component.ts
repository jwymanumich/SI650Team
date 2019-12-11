import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NgxSpinnerService } from "ngx-spinner";
import { CloudData, CloudOptions } from 'angular-tag-cloud-module';
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

  options: CloudOptions = {
    width: 400,
    height: 400,
    overflow: true,
    randomizeAngle: true
  };

  colors: string[] = ['#fabebe', '#ffd8b1', '#fffac8', '#aaffc3', '#e6beff',
    '#668fff', '#91fbff', '#a1a1a1', '#ffd8b1', '#fabebe'];
  data0: CloudData[] = [];
  data1: CloudData[] = [];
  data2: CloudData[] = [];
  data3: CloudData[] = [];
  data4: CloudData[] = [];

  constructor(private route: ActivatedRoute,
    private twitterService: TwitterTopicService,
    private spinner: NgxSpinnerService) { }

  ngOnInit() {
    this.handle = this.route.snapshot.paramMap.get('id');
    this.getLexSummary();
    this.getWordCloud();
  }

  getWordCloud() {
    this.twitterService.getTwitterTopics(this.handle.replace('@', '')).subscribe(result => {
      // Colors
      result.forEach(cloud => {
        cloud.words.forEach((word, i) => {
          word.color = this.colors[i];
        });
      });

      // Word Clouds
      this.data0 = result[0].words;
      this.data1 = result[1].words;
      this.data2 = result[2].words;
      this.data3 = result[3].words;
      this.data4 = result[4].words;
    });
  }

  tabClick(tab) {
    const idx = tab.index;
    if (idx == 0) { // LexRank
      this.getLexSummary();
    } else if (idx == 1) { // LatentDirichletAllocation
      this.getLdaSummary();
    } else { // Random
      this.getRanSummary();
    }
  }

  getLexSummary() {
    if (this.lexTweets) return;
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
    if (this.ldaTweets) return;
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
    if (this.ranTweets) return;
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

import { ApplicationRef, Component, OnDestroy, Input, ElementRef, QueryList, ViewChild, OnInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TwitterTopicService } from '../twitter_topic/twitter_topic.service';
import { AgWordCloudDirective } from '../../../node_modules/angular4-word-cloud/ag-wordcloud.directive'
import { NgxTweetComponent } from '../../../node_modules/ngx-tweet'
import { Router, NavigationEnd } from '@angular/router';


@Component({
  selector: 'app-summary',
  templateUrl: './summary.component.html',
  styleUrls: ['./summary.component.css'],
  providers: [TwitterTopicService]
})

export class SummaryComponent implements OnInit {
  @ViewChild('cloudchart1', {static: false}) cloudchart1: AgWordCloudDirective
  @ViewChild('cloudchart2', {static: false}) cloudchart2: AgWordCloudDirective
  @ViewChild('cloudchart3', {static: false}) cloudchart3: AgWordCloudDirective
  @ViewChild('cloudchart4', {static: false}) cloudchart4: AgWordCloudDirective
  @ViewChild('cloudchart5', {static: false}) cloudchart5: AgWordCloudDirective

  @ViewChild('viewtweet1', {static: true}) viewtweet1: NgxTweetComponent
  @ViewChild('myDiv', {static: true}) divView: ElementRef;

  public handle: string;
  public body: string = "921670221710032896";
  public tweet_1: string;
  public appref: ApplicationRef;
  private twitter: any;

  wordData1: any = [];
  wordData2: any = [];
  wordData3: any = [];
  wordData4: any = [];
  wordData5: any = [];

  wordData: any = [];
  options: any = {};

  //constructor(appRef: ApplicationRef) {}

  constructor(private _router: Router, private route: ActivatedRoute, private twittertopicservice: TwitterTopicService, appRef: ApplicationRef) { 

    this.wordData1 = [
        {size: 50, text: ''}
    ]
    this.wordData2 = [
        {size: 50, text: ''}
    ]
    this.wordData3 = [
        {size: 50, text: ''}
    ]
    this.wordData4 = [
        {size: 50, text: ''}
    ]
    this.wordData5 = [
        {size: 50, text: ''}
    ]

    this.wordData = [
        {size: 50, text: ''},
   ];
  
   this.appref = appRef;
    this.options = {
        settings: {
        minFontSize: 10,
        maxFontSize: 100,
        },
        margin: {
            top: 10,
            right: 10,
            bottom: 10,
            left: 10
        },
        labels: true // false to hide hover labels
    };
  }

  initTwitterWidget() {
    this.twitter = this._router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        (<any>window).twttr = (function (d, s, id) {
          let js: any, fjs = d.getElementsByTagName(s)[0],
              t = (<any>window).twttr || {};
          if (d.getElementById(id)) return t;
          js = d.createElement(s);
          js.id = id;
          js.src = "https://platform.twitter.com/widgets.js";
          fjs.parentNode.insertBefore(js, fjs);

          t._e = [];
          t.ready = function (f: any) {
              t._e.push(f);
          };

          return t;
        }(document, "script", "twitter-wjs"));

        if ((<any>window).twttr.ready())
          (<any>window).twttr.widgets.load();

      }
    });
  }

  ngOnDestroy() {
    this.twitter.unsubscribe();
  }

  ngOnInit() {
      this.handle = this.route.snapshot.paramMap.get('id');

      var a = this.twittertopicservice.getTwitterTopics(this.handle).subscribe((x: string) => {

          for (let my_topic of x[0]) {
              console.log(my_topic); 
              this.wordData1.push({size: my_topic["weight"], text: my_topic["word"]})
          }
          for (let my_topic of x[1]) {
            console.log(my_topic); 
            this.wordData2.push({size: my_topic["weight"], text: my_topic["word"]})
        }
        for (let my_topic of x[2]) {
            console.log(my_topic); 
            this.wordData3.push({size: my_topic["weight"], text: my_topic["word"]})
        }
        for (let my_topic of x[3]) {
            console.log(my_topic); 
            this.wordData4.push({size: my_topic["weight"], text: my_topic["word"]})
        }
        for (let my_topic of x[4]) {
            console.log(my_topic); 
            this.wordData5.push({size: my_topic["weight"], text: my_topic["word"]})
        }



        //          this.cloudchart.wordData.push({size: 555, text: 'ASDF'})
          this.cloudchart1.update();
          this.cloudchart2.update();
          this.cloudchart3.update();
          this.cloudchart4.update();
          this.cloudchart5.update();
      })

      var a = this.twittertopicservice.getTwitterTopTweets(this.handle).subscribe((x: string) => {
//        console.log(x); 
        this.body = x['values'][0]['id'];
//        this.viewtweet1.refresh();
//        this.viewtweet1.size(500, 233);
      //  this.appref.tick();

        this.twitter.widgets.load()

//       this.divView.nativeElement.innerHTML = "<div #myDiv><ngx-tweet tweetId=" + this.body + "></ngx-tweet></div>";
//        this.divView.nativeElement.OnInit();
//    private _loadTwitterScript();
//private _updateTwitterScriptLoadingState();


        })
    }
}
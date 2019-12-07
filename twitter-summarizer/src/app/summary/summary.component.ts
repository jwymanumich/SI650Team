import { Component, Input, ElementRef, QueryList, ViewChild, OnInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TwitterTopicService } from '../twitter_topic/twitter_topic.service';
import { AgWordCloudDirective } from '../../../node_modules/angular4-word-cloud/ag-wordcloud.directive'

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

  public handle: string;
  public body: string;

  wordData1: any = [];
  wordData2: any = [];
  wordData3: any = [];
  wordData4: any = [];
  wordData5: any = [];

  wordData: any = [];
  options: any = {};

  
  constructor(private route: ActivatedRoute, private twittertopicservice: TwitterTopicService) { 

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
        // {size: 950, text: 'Angular'},
        // {size: 123, text: 'JAva script'},
        // {size: 321, text: 'ngServe'},
        // {size: 231, text: 'Int'},
        // {size: 123, text: 'CkEditor'},
        // {size: 346, text: 'Ng Model'},
        // {size: 107, text: 'Variable'},
        // {size: 436, text: 'Class'},
        // {size: 731, text: 'NgOnInit'},
        // {size: 80, text: '@Input'},
        // {size: 96, text: '@Output'},
        // {size: 531, text: 'EventEmitter'},
        // {size: 109, text: 'ChangeDetection'},
        // {size: 500, text: 'Directives'},
        // {size: 213, text: 'Services'},
        // {size: 294, text: 'Component'},
        // {size: 472, text: 'NgViewAfterInIt'},
        // {size: 297, text: 'NgOnChanges'},
        // {size: 456, text: 'NgBind'},
        // {size: 123, text: 'NgTest'},
        // {size: 376, text: 'Pipes'},
        // {size: 93, text: 'Implements'},
        // {size: 123, text: 'Assets'},
   ];
  
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
    }
}
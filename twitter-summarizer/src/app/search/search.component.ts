import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TwitterTopicService } from '../twitter_topic/twitter_topic.service';
    
@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
  providers: [TwitterTopicService]
})

export class SearchComponent implements OnInit {

  title: string = 'Twitzer';

  placeholder: string = '@Matt_LeBlanc';

  handle: string;

  mystring: string;

  constructor(private router: Router, private twittertopicservice: TwitterTopicService) { }

  ngOnInit() {
  }

  checkPlaceHolder() {
    if (this.placeholder) {
      this.placeholder = null;
      return;
    } else {
      this.placeholder = '@Matt_LeBlanc';
      return;
    }
  }

  async search() {
    console.log(`/summary/${this.handle}`);
//    var a = this.twittertopicservice.getTwitterTopics()
    
//    var a = this.twittertopicservice.getTwitterTopics().subscribe((x: string) => {
//                  this.title = x;
//                  this.placeholder = x;
//                  this.handle = x;
//    })

//    .subscribe((e: KeyboardEvent) => {
//        if (e.keyCode === ESC_KEY) {
//          nameInput.value = '';
//        }

    console.log('afff'); 
    this.router.navigateByUrl(`/summary/${this.handle}`);
  }

  searchRandom() {
    console.log(`/summary/random`);
    this.router.navigateByUrl(`/summary/random`);
  }
}

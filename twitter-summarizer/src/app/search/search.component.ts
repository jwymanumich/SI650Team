import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  title = 'Twitzer';

  placeholder: string = '@Matt_LeBlanc';

  handle: string;

  handles: string[] = ['@elonmusk', '@barackobama', '@realdonaldtrump', '@justinbieber', '@neiltyson', '@wendys',
    '@gordonramsay', '@katyperry'];

  constructor(private router: Router) { }

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

  search() {
    console.log(`/summary/${this.handle}`);
    this.router.navigateByUrl(`/summary/${this.handle}`);
  }

  searchRandom() {
    const idx = Math.floor(Math.random() * this.handles.length) + 0 
    this.handle = this.handles[idx];
    this.search();
  }
}

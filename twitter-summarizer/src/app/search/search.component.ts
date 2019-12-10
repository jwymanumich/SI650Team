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
    console.log(`/summary/random`);
    this.router.navigateByUrl(`/summary/random`);
  }
}

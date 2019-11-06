import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-summary',
  templateUrl: './summary.component.html',
  styleUrls: ['./summary.component.css']
})
export class SummaryComponent implements OnInit {

  public handle: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.handle = this.route.snapshot.paramMap.get('id');
  }
}

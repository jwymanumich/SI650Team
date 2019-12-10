// branch: michaelalvin

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSliderModule } from '@angular/material/slider';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { NgxTweetModule } from "ngx-tweet";
import { HttpClientModule } from '@angular/common/http';

import { ToolbarComponent } from './toolbar/toolbar.component';
import { SearchComponent } from './search/search.component';
import { SummaryComponent } from './summary/summary.component';
import { TwitterTopicService } from './twitter_topic/twitter_topic.service';
import {AgWordCloudModule, AgWordCloudData} from 'angular4-word-cloud';


@NgModule({
  providers: [
    TwitterTopicService
  ],
  declarations: [
    AppComponent,
    ToolbarComponent,
    SearchComponent,
    SummaryComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSliderModule,
    MatToolbarModule,
    MatInputModule,
    MatButtonModule,
    FormsModule,
    HttpClientModule,
    NgxTweetModule,
    AgWordCloudModule.forRoot()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

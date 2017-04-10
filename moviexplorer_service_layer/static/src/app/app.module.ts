import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { HttpModule, JsonpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';

import { TruncatePipe } from './pipes/text-truncate.pipe';

import { SlimLoadingBarModule } from 'ng2-slim-loading-bar';

import { AppComponent }  from './app.component';
import { MovieComponent }  from './movie/movie.component';

@NgModule({
  imports:      [ BrowserModule, HttpModule, JsonpModule,
                  SlimLoadingBarModule.forRoot(), FormsModule],
  declarations: [ AppComponent, MovieComponent, TruncatePipe],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }

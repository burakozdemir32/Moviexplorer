import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule, JsonpModule } from '@angular/http';

import { TruncatePipe } from './pipes/text-truncate.pipe';

import { AppComponent }  from './app.component';
import { MovieComponent }  from './movie/movie.component';

@NgModule({
  imports:      [ BrowserModule, HttpModule, JsonpModule ],
  declarations: [ AppComponent, MovieComponent, TruncatePipe],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }

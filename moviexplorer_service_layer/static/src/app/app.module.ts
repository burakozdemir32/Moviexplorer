import { NgModule }      from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule, JsonpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { TruncatePipe } from './pipes/text-truncate.pipe';
import { SlimLoadingBarModule } from 'ng2-slim-loading-bar';
import { Ng2Bs3ModalModule } from 'ng2-bs3-modal/ng2-bs3-modal';
import { AppComponent }  from './app.component';
import { MovieComponent }  from './movie/movie.component';
import { RecommendationsComponent }  from './recommendations/recommendations.component';

const router: Routes = [
    {path: '', component: MovieComponent},
    {path: 'recommendations', component: RecommendationsComponent}
];

const routing = RouterModule.forRoot(router);

@NgModule({
  imports:      [ BrowserModule, HttpModule, JsonpModule, FormsModule,
                  SlimLoadingBarModule.forRoot(), Ng2Bs3ModalModule, routing],
  declarations: [ AppComponent, MovieComponent, RecommendationsComponent, TruncatePipe],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }

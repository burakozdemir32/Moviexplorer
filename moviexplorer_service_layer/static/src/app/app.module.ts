import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule, JsonpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { TruncatePipe } from './pipes/text-truncate.pipe';
import { SlimLoadingBarModule } from 'ng2-slim-loading-bar';
import { Ng2Bs3ModalModule } from 'ng2-bs3-modal/ng2-bs3-modal';
import { ReactiveFormsModule } from '@angular/forms';
import { StarRatingModule } from 'angular-star-rating';

import { AppComponent }  from './app.component';
import { MovieComponent }  from './movie/movie.component';
import { RatingComponent }  from './rating/rating.component';
import { RecommendationsComponent }  from './recommendations/recommendations.component';

import { routing, appRoutingProviders } from  './app.routing';
import { AuthGuard } from './guards/auth.guard';
import { AuthService } from './services/auth.service';

@NgModule({
  imports:      [ BrowserModule, HttpModule, JsonpModule, FormsModule,
                  SlimLoadingBarModule.forRoot(), Ng2Bs3ModalModule, routing, ReactiveFormsModule, StarRatingModule],
  declarations: [ AppComponent, MovieComponent, RatingComponent, RecommendationsComponent, TruncatePipe],
  bootstrap:    [ AppComponent ],
  providers: [ appRoutingProviders, AuthGuard, AuthService ]
})
export class AppModule { }

import { Component } from '@angular/core';
import { MovieService } from '../services/movie.service';
import {SlimLoadingBarService} from 'ng2-slim-loading-bar';

@Component({
    moduleId: module.id,
    selector: 'movie-cmp',
    templateUrl: 'movie.component.html'
})
export class MovieComponent  {
    topMovieList: Array<Object>;

    constructor(private movieService: MovieService, private slimLoader: SlimLoadingBarService) {

    }

    ngOnInit(): any {
        this.slimLoader.start();
        this.movieService.getTopMovies().subscribe( res => {
            this.topMovieList = res.results;
        }, (error: any) => {
            console.log('Error occured while fetching movies.')
        }, () => {
            this.slimLoader.complete();
        });
    }
}


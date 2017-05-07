import { Component } from '@angular/core';
import { MovieService } from '../services/movie.service';
import { SlimLoadingBarService } from 'ng2-slim-loading-bar';
import { Subject } from 'rxjs/Subject';

@Component({
    moduleId: module.id,
    selector: 'movie-cmp',
    templateUrl: 'movie.component.html'
})
export class MovieComponent  {
    topMovieList: Array<Object>;
    movieSearchResults: Array<Object>;
    title$ = new Subject<string>();

    constructor(private movieService: MovieService, private slimLoader: SlimLoadingBarService) {

    }

    searchMovie(title: string) {
        this.slimLoader.start();
        this.movieService.searchMovie(title)
            .subscribe(res => this.movieSearchResults = res.results,
                (error: any) => console.log(error),
                () => this.slimLoader.complete()
            );
    }

    ngOnInit(): any {

    }
}


import { Component } from '@angular/core';
import { MovieService } from '../services/movie.service';
import { AuthService } from '../services/auth.service';
import { SlimLoadingBarService } from 'ng2-slim-loading-bar';

@Component({
    moduleId: module.id,
    selector: 'movie-cmp',
    templateUrl: 'movie.component.html'
})
export class MovieComponent  {
    movieSearchResults: Array<Object>;

    constructor(private movieService: MovieService, public authService: AuthService, private slimLoader: SlimLoadingBarService) {

    }

    searchMovie(title: string) {
        this.slimLoader.start();
        this.movieService.searchMovie(title)
            .subscribe(res => this.movieSearchResults = res.results,
                (error: any) => console.log(error),
                () => this.slimLoader.complete()
            );
    }
}


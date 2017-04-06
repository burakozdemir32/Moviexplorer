import { Component } from '@angular/core';
import { MovieService } from '../services/movie.service';

@Component({
    moduleId: module.id,
    selector: 'movie-cmp',
    templateUrl: 'movie.component.html'
})
export class MovieComponent  {
    topMovieList: Array<Object>;

    constructor(private movieService: MovieService) {
        this.movieService.getTopMovies().subscribe( res => {
            this.topMovieList = res.results;
            console.log(res.results)
        })

    }
}


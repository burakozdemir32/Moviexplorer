import { Component } from '@angular/core';
import { MovieService } from '../services/movie.service';

@Component({
    moduleId: module.id,
    selector: 'movie-cmp',
    templateUrl: 'movie.component.html'
})
export class MovieComponent  {
    constructor(private movieService: MovieService) {

    }
}

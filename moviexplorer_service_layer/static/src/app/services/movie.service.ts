import { Injectable } from '@angular/core';
import { Jsonp } from '@angular/http';
import 'rxjs/Rx';

@Injectable()
export class MovieService{
    private apiURL = 'http://127.0.0.1:8000/api/movies?callback=JSONP_CALLBACK';

    constructor(private jsonp: Jsonp) {
        console.log('Movie service initialised.')
    }

    getTopMovies() {
        return this.jsonp.get(this.apiURL)
            .map(res => res.json());
    }

}
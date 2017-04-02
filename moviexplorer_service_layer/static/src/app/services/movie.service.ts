import { Injectable } from '@angular/core';
import { Jsonp } from '@angular/http';
import 'rxjs/Rx';

@Injectable()
export class MovieService{
    constructor(private jsonp: Jsonp) {
        console.log('MovieService Initialised...');
    }

    getTopMovies() {
        this.jsonp.get('');
    }
}
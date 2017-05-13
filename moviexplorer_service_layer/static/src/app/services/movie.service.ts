import { Injectable } from '@angular/core';
import { Jsonp, URLSearchParams } from '@angular/http';
import 'rxjs/Rx';

@Injectable()
export class MovieService {
    private apiURL = 'http://127.0.0.1:8000/api/';

    constructor(private jsonp: Jsonp) {
        console.log('Movie service initialised.');
    }

    searchMovie(title: string) {
        let search = new URLSearchParams();
        search.set('action', 'opensearch');
        search.set('title', title);

        return this.jsonp.get(this.apiURL + 'movies?callback=JSONP_CALLBACK', {search})
            .map(res => res.json());

    }

    getRecommendations(user_id: string) {
        let search = new URLSearchParams();
        search.set('action', 'opensearch');
        search.set('user_id', user_id);

        return this.jsonp.get(this.apiURL + 'recommendations?callback=JSONP_CALLBACK', {search})
            .map(res => res.json());

    }
}

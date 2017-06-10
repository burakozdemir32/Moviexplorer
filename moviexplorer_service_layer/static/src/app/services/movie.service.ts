import { Injectable } from '@angular/core';
import { Jsonp, URLSearchParams, Headers, Http } from '@angular/http';
import 'rxjs/Rx';

@Injectable()
export class MovieService {
    private apiURL = 'http://127.0.0.1:8000/api/';

    constructor(private jsonp: Jsonp, private http: Http ) {
    }

    searchMovie(title: string) {
        let search = new URLSearchParams();
        search.set('title', title);

        return this.jsonp.get(this.apiURL + 'movies?callback=JSONP_CALLBACK', {search: search})
            .map(res => res.json());

    }

    getRecommendations(user_id: string) {
        let search = new URLSearchParams();
        search.set('user_id', user_id);

        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        let token = currentUser.token;

        let headers = new Headers();
        headers.set('Authorization', 'JWT ' + token);

        return this.http.get(this.apiURL + 'recommendations/', {headers: headers, search: search})
            .map(res => res.json());

    }
}

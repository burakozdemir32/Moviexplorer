import { Injectable } from '@angular/core';
import { Jsonp, URLSearchParams, Headers, Http } from '@angular/http';
import 'rxjs/Rx';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

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

    getRecommendations() {
        let search = new URLSearchParams();

        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        let token = currentUser.token;
        let username = currentUser.username;
        search.set('username', username);

        let headers = new Headers();
        headers.set('Authorization', 'JWT ' + token);

        return this.http.get(this.apiURL + 'recommendations/', {headers: headers, search: search})
            .map(res => res.json());

    }
}

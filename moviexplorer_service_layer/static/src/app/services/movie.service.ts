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
    private rateURL = 'http://127.0.0.1:8000/api/rate/';
    private headers = new Headers({'Content-Type': 'application/json'});

    constructor(private jsonp: Jsonp, private http: Http ) {
    }

    searchMovie(title: string) {
        let search = new URLSearchParams();
        search.set('title', title);

        return this.jsonp.get(this.apiURL + 'movies?callback=JSONP_CALLBACK', {search: search})
            .map(res => res.json());

    }

    rateMovie(currentUser: any, rating: number, movie_id: number): Observable<any> {
        let body = JSON.stringify({
                username: currentUser.username,
                rating: rating,
                movie: movie_id
            }
        );

        this.headers.set('Authorization', 'JWT ' + currentUser.token);
        return this.http.post(this.rateURL, body, {headers: this.headers})
            .map(response => {
                if (response.json().id) {
                    return true;
                } else {
                    return false;
                }
            })
            .catch((error: any) => Observable.throw(error.json() || 'Server error'));
    }

    getRecommendations(currentUser: any) {
        let search = new URLSearchParams();
        search.set('username', currentUser.username);

        let headers = new Headers();
        headers.set('Authorization', 'JWT ' + currentUser.token);

        return this.http.get(this.apiURL + 'recommendations/', {headers: headers, search: search})
            .map(res => res.json());

    }
}

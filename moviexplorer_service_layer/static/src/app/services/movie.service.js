"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require("@angular/core");
var http_1 = require("@angular/http");
require("rxjs/Rx");
var Rx_1 = require("rxjs/Rx");
require("rxjs/add/operator/map");
require("rxjs/add/operator/catch");
require("rxjs/add/observable/throw");
var MovieService = (function () {
    function MovieService(jsonp, http) {
        this.jsonp = jsonp;
        this.http = http;
        this.apiURL = 'http://127.0.0.1:8000/api/';
        this.rateURL = 'http://127.0.0.1:8000/api/rate/';
        this.headers = new http_1.Headers({ 'Content-Type': 'application/json' });
    }
    MovieService.prototype.searchMovie = function (title) {
        var search = new http_1.URLSearchParams();
        search.set('title', title);
        return this.jsonp.get(this.apiURL + 'movies?callback=JSONP_CALLBACK', { search: search })
            .map(function (res) { return res.json(); });
    };
    MovieService.prototype.rateMovie = function (currentUser, rating, movie_id) {
        var body = JSON.stringify({
            username: currentUser.username,
            rating: rating,
            movie: movie_id
        });
        this.headers.set('Authorization', 'JWT ' + currentUser.token);
        return this.http.post(this.rateURL, body, { headers: this.headers })
            .map(function (response) {
            if (response.json().id) {
                return true;
            }
            else {
                return false;
            }
        })
            .catch(function (error) { return Rx_1.Observable.throw(error.json() || 'Server error'); });
    };
    MovieService.prototype.getRecommendations = function (currentUser) {
        var search = new http_1.URLSearchParams();
        search.set('username', currentUser.username);
        var headers = new http_1.Headers();
        headers.set('Authorization', 'JWT ' + currentUser.token);
        return this.http.get(this.apiURL + 'recommendations/', { headers: headers, search: search })
            .map(function (res) { return res.json(); });
    };
    return MovieService;
}());
MovieService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [http_1.Jsonp, http_1.Http])
], MovieService);
exports.MovieService = MovieService;
//# sourceMappingURL=movie.service.js.map
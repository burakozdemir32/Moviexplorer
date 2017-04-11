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
Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = require("@angular/core");
var http_1 = require("@angular/http");
require("rxjs/Rx");
var MovieService = (function () {
    function MovieService(jsonp) {
        this.jsonp = jsonp;
        this.apiURL = 'http://127.0.0.1:8000/api/movies?callback=JSONP_CALLBACK';
        console.log('Movie service initialised.');
    }
    MovieService.prototype.getTopMovies = function () {
        return this.jsonp.get(this.apiURL)
            .map(function (res) { return res.json(); });
    };
    MovieService.prototype.searchMovie = function (title) {
        var search = new http_1.URLSearchParams();
        search.set('action', 'opensearch');
        search.set('title', title);
        return this.jsonp.get(this.apiURL, { search: search })
            .map(function (res) { return res.json(); });
    };
    return MovieService;
}());
MovieService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [http_1.Jsonp])
], MovieService);
exports.MovieService = MovieService;
//# sourceMappingURL=movie.service.js.map
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
var movie_service_1 = require("../services/movie.service");
var auth_service_1 = require("../services/auth.service");
var ng2_slim_loading_bar_1 = require("ng2-slim-loading-bar");
var MovieComponent = (function () {
    function MovieComponent(movieService, authService, slimLoader) {
        this.movieService = movieService;
        this.authService = authService;
        this.slimLoader = slimLoader;
    }
    MovieComponent.prototype.searchMovie = function (title) {
        var _this = this;
        this.slimLoader.start();
        this.movieService.searchMovie(title)
            .subscribe(function (res) { return _this.movieSearchResults = res.results; }, function (error) { return console.log(error); }, function () { return _this.slimLoader.complete(); });
    };
    return MovieComponent;
}());
MovieComponent = __decorate([
    core_1.Component({
        moduleId: module.id,
        selector: 'movie-cmp',
        templateUrl: 'movie.component.html'
    }),
    __metadata("design:paramtypes", [movie_service_1.MovieService, auth_service_1.AuthService, ng2_slim_loading_bar_1.SlimLoadingBarService])
], MovieComponent);
exports.MovieComponent = MovieComponent;
//# sourceMappingURL=movie.component.js.map
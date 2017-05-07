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
var ng2_bs3_modal_1 = require("ng2-bs3-modal/ng2-bs3-modal");
var movie_service_1 = require("./services/movie.service");
var auth_service_1 = require("./services/auth.service");
var AppComponent = (function () {
    function AppComponent(authService) {
        this.authService = authService;
        this.userCredentials = {
            username: '',
            password: ''
        };
        this.error = '';
    }
    // Modal methods.
    AppComponent.prototype.closeModal = function () {
        this.loginModal.close();
    };
    AppComponent.prototype.openModal = function () {
        this.loginModal.open();
    };
    // Authentication.
    AppComponent.prototype.login = function () {
        var _this = this;
        this.authService.login(this.userCredentials)
            .subscribe(function (result) {
            if (result === true) {
                _this.closeModal();
            }
            else {
                _this.error = 'Username or password is incorrect';
            }
        }, function (error) {
            _this.error = error;
        });
    };
    return AppComponent;
}());
__decorate([
    core_1.ViewChild('loginModal'),
    __metadata("design:type", ng2_bs3_modal_1.ModalComponent)
], AppComponent.prototype, "loginModal", void 0);
AppComponent = __decorate([
    core_1.Component({
        moduleId: module.id,
        selector: 'app-cmp',
        templateUrl: 'app.component.html',
        providers: [movie_service_1.MovieService, auth_service_1.AuthService]
    }),
    __metadata("design:paramtypes", [auth_service_1.AuthService])
], AppComponent);
exports.AppComponent = AppComponent;
//# sourceMappingURL=app.component.js.map
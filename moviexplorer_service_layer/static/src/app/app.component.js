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
var router_1 = require("@angular/router");
var movie_service_1 = require("./services/movie.service");
var auth_service_1 = require("./services/auth.service");
var forms_1 = require("@angular/forms");
var AppComponent = (function () {
    function AppComponent(authService, router, fb) {
        this.authService = authService;
        this.router = router;
        this.fb = fb;
        this.userCredentials = {
            username: '',
            password: ''
        };
        this.error = false;
        this.isLoggedIn = false;
        this.showLoginField = true;
        // Register form configurations
        this.userInformation = {
            username: '',
            email: '',
            password: ''
        };
        this.formErrors = {
            'username': '',
            'email': '',
            'password': '',
            'confirmPassword': ''
        };
        this.validationMessages = {
            'username': {
                'required': 'Username is required.',
                'minlength': 'Username must be at least 4 characters long.',
                'maxlength': 'Username cannot be more than 24 characters long.'
            },
            'email': {
                'email': 'Enter a valid email address.'
            },
            'password': {
                'required': 'Password is required.'
            },
            'confirmPassword': {
                'required': 'Confirm is required.',
                'MatchPassword': 'Needs'
            }
        };
        if (localStorage.getItem('currentUser')) {
            this.isLoggedIn = true;
            this.authService.isLoggedIn = true;
        }
    }
    AppComponent.prototype.ngOnInit = function () {
        this.buildForm();
    };
    // Modal methods.
    AppComponent.prototype.closeModal = function () {
        this.loginModal.close();
    };
    AppComponent.prototype.openModal = function () {
        this.error = false;
        this.showLoginField = true;
        this.loginModal.open();
    };
    // Authentication.
    AppComponent.prototype.login = function () {
        var _this = this;
        this.authService.login(this.userCredentials)
            .subscribe(function (result) {
            if (result === true) {
                _this.isLoggedIn = true;
                _this.closeModal();
            }
            else {
                _this.error = true;
            }
        }, function (error) {
            _this.error = true;
        });
    };
    AppComponent.prototype.logout = function () {
        this.authService.logout();
        this.isLoggedIn = false;
        this.router.navigate(['']);
    };
    AppComponent.prototype.submitRegisterForm = function () {
        var _this = this;
        this.authService.register(this.userInformation)
            .subscribe(function (result) {
            if (result === true) {
                _this.closeModal();
            }
            else {
                _this.error = true;
            }
        }, function (error) {
            if (error.hasOwnProperty('email')) {
                console.log(error.email[0]);
            }
            else if (error.hasOwnProperty('email') && error.hasOwnProperty('username')) {
                console.log(error.email[0]);
                console.log(error.username[0]);
            }
            else {
                console.log(error);
            }
            _this.error = true;
        });
    };
    AppComponent.prototype.resetForms = function () {
        this.loginForm.reset();
        this.registerForm.reset();
    };
    AppComponent.prototype.buildForm = function () {
        var _this = this;
        this.registerForm = this.fb.group({
            'username': [null, [
                    forms_1.Validators.required,
                    forms_1.Validators.minLength(4),
                    forms_1.Validators.maxLength(24)
                ]
            ],
            'email': [null, [
                    forms_1.Validators.email,
                ]
            ],
            'password': [null, forms_1.Validators.required],
            'confirmPassword': [null, forms_1.Validators.required]
        }, { validator: this.matchPassword });
        this.registerForm.valueChanges
            .subscribe(function (data) { return _this.onValueChanged(data); });
        this.onValueChanged(); // (re)set validation messages now
        this.loginForm = this.fb.group({
            'username': [null, forms_1.Validators.required],
            'password': [null, forms_1.Validators.required]
        });
    };
    AppComponent.prototype.matchPassword = function (AC) {
        var password = AC.get('password').value;
        var confirmPassword = AC.get('confirmPassword').value;
        if (password !== confirmPassword) {
            AC.get('confirmPassword').setErrors({ MatchPassword: true });
        }
        else {
            AC.get('confirmPassword').setErrors(null);
        }
        return null;
    };
    AppComponent.prototype.onValueChanged = function (data) {
        if (!this.registerForm) {
            return;
        }
        var form = this.registerForm;
        for (var field in this.formErrors) {
            // clear previous error message (if any)
            this.formErrors[field] = '';
            var control = form.get(field);
            if (control && control.dirty && !control.valid) {
                var messages = this.validationMessages[field];
                for (var key in control.errors) {
                    this.formErrors[field] += messages[key] + ' ';
                }
            }
        }
    };
    return AppComponent;
}());
__decorate([
    core_1.ViewChild(ng2_bs3_modal_1.ModalComponent),
    __metadata("design:type", ng2_bs3_modal_1.ModalComponent)
], AppComponent.prototype, "loginModal", void 0);
AppComponent = __decorate([
    core_1.Component({
        moduleId: module.id,
        selector: 'app-cmp',
        templateUrl: 'app.component.html',
        providers: [movie_service_1.MovieService]
    }),
    __metadata("design:paramtypes", [auth_service_1.AuthService, router_1.Router, forms_1.FormBuilder])
], AppComponent);
exports.AppComponent = AppComponent;
//# sourceMappingURL=app.component.js.map
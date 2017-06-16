import { Component, ViewChild } from '@angular/core';
import { ModalComponent } from 'ng2-bs3-modal/ng2-bs3-modal';
import { Router } from '@angular/router';
import { MovieService } from './services/movie.service';
import { AuthService } from './services/auth.service';
import {FormBuilder, FormGroup, Validators, AbstractControl} from '@angular/forms';

@Component({
    moduleId: module.id,
    selector: 'app-cmp',
    templateUrl: 'app.component.html',
    providers: [ MovieService ]
})

// TODO Seperate AppComponent. (into LoginComponent and RegisterComponent)
export class AppComponent {
    @ViewChild(ModalComponent)
    private loginModal: ModalComponent;

    loginForm: FormGroup;
    userCredentials = {
        username: '',
        password: ''
    };
    error = false;
    isLoggedIn = false;
    showLoginField = true;

    // Register form configurations
    userInformation = {
        username: '',
        email: '',
        password: ''
    };
    registerForm: FormGroup;
    formErrors = {
        'username': '',
        'email': '',
        'password': '',
        'confirmPassword': ''
    };
    validationMessages = {
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

    constructor(private authService: AuthService, private router: Router, private fb: FormBuilder) {
        if (localStorage.getItem('currentUser')) {
            this.isLoggedIn = true;
        }
    }

    ngOnInit(): void {
        this.buildForm();
    }

    // Modal methods.
    closeModal() {
        this.loginModal.close();
    }

    openModal() {
        this.error = false;
        this.showLoginField = true;
        this.loginModal.open();
    }

    // Authentication.
    login() {
        this.authService.login(this.userCredentials)
            .subscribe(result => {
                if (result === true) {
                    this.isLoggedIn = true;
                    this.closeModal();
                } else {
                    this.error = true;
                }
            }, error => {
                this.error = true;
            });
    }

    logout() {
        this.authService.logout();
        this.isLoggedIn = false;
        this.router.navigate(['']);
    }

    submitRegisterForm() {
        this.authService.register(this.userInformation)
            .subscribe(result => {
                if (result === true) {
                    this.closeModal();
                } else {
                    this.error = true;
                }
            }, error => {
                if (error.hasOwnProperty('email')) {
                    console.log(error.email[0]);
                } else if (error.hasOwnProperty('email') && error.hasOwnProperty('username')) {
                    console.log(error.email[0]);
                    console.log(error.username[0]);
                } else {
                    console.log(error);
                }
                this.error = true;
            });
    }

    resetForms(): void {
        this.loginForm.reset();
        this.registerForm.reset();
    }

    buildForm(): void {
        this.registerForm = this.fb.group({
            'username': [null, [
                Validators.required,
                Validators.minLength(4),
                Validators.maxLength(24)]
            ],
            'email': [null, [
                Validators.email,
                ]
            ],
            'password': [null, Validators.required],
            'confirmPassword': [null, Validators.required]
        }, {validator: this.matchPassword});

        this.registerForm.valueChanges
            .subscribe(data => this.onValueChanged(data));

        this.onValueChanged(); // (re)set validation messages now

        this.loginForm = this.fb.group({
            'username': [null, Validators.required],
            'password': [null, Validators.required]});
    }

    matchPassword(AC: AbstractControl): any {
       let password = AC.get('password').value;
       let confirmPassword = AC.get('confirmPassword').value;

       if (password !== confirmPassword) {
            AC.get('confirmPassword').setErrors( {MatchPassword: true});
       } else {
            AC.get('confirmPassword').setErrors(null);
       }
       return null;
    }

    onValueChanged(data?: any) {
        if (!this.registerForm) { return; }
        const form = this.registerForm;

        for (const field in this.formErrors) {
          // clear previous error message (if any)
            this.formErrors[field] = '';
            const control = form.get(field);

            if (control && control.dirty && !control.valid) {
                const messages = this.validationMessages[field];

                for (const key in control.errors) {
                    this.formErrors[field] += messages[key] + ' ';
                }
            }
        }
      }
}

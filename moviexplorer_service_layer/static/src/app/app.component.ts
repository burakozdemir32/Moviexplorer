import { Component, ViewChild } from '@angular/core';
import {ModalComponent} from 'ng2-bs3-modal/ng2-bs3-modal';

import {MovieService} from './services/movie.service';
import {AuthService} from './services/auth.service';

@Component({
    moduleId: module.id,
    selector: 'app-cmp',
    templateUrl: 'app.component.html',
    providers: [ MovieService, AuthService ]
})
export class AppComponent {
    @ViewChild(ModalComponent)
    private loginModal: ModalComponent;

    userCredentials = {
        username: '',
        password: ''
    };
    error = false;
    isLoggedIn = false;

    constructor(private authService: AuthService) {
    }
    // Modal methods.
    closeModal() {
        this.loginModal.close();
    }

    openModal() {
        this.error = false;
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
}
import { Component } from '@angular/core';
import { MovieService } from './services/movie.service';
import { Subject } from 'rxjs/Subject';

@Component({
    moduleId: module.id,
    selector: 'app-cmp',
    templateUrl: 'app.component.html',
    providers: [ MovieService ]
})
export class AppComponent  {}

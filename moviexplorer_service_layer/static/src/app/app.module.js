"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var core_1 = require("@angular/core");
var platform_browser_1 = require("@angular/platform-browser");
var http_1 = require("@angular/http");
var forms_1 = require("@angular/forms");
var text_truncate_pipe_1 = require("./pipes/text-truncate.pipe");
var ng2_slim_loading_bar_1 = require("ng2-slim-loading-bar");
var ng2_bs3_modal_1 = require("ng2-bs3-modal/ng2-bs3-modal");
var app_component_1 = require("./app.component");
var movie_component_1 = require("./movie/movie.component");
var recommendations_component_1 = require("./recommendations/recommendations.component");
var app_routing_1 = require("./app.routing");
var auth_guard_1 = require("./guards/auth.guard");
var forms_2 = require("@angular/forms");
var AppModule = (function () {
    function AppModule() {
    }
    return AppModule;
}());
AppModule = __decorate([
    core_1.NgModule({
        imports: [platform_browser_1.BrowserModule, http_1.HttpModule, http_1.JsonpModule, forms_1.FormsModule,
            ng2_slim_loading_bar_1.SlimLoadingBarModule.forRoot(), ng2_bs3_modal_1.Ng2Bs3ModalModule, app_routing_1.routing, forms_2.ReactiveFormsModule],
        declarations: [app_component_1.AppComponent, movie_component_1.MovieComponent, recommendations_component_1.RecommendationsComponent, text_truncate_pipe_1.TruncatePipe],
        bootstrap: [app_component_1.AppComponent],
        providers: [app_routing_1.appRoutingProviders, auth_guard_1.AuthGuard]
    })
], AppModule);
exports.AppModule = AppModule;
//# sourceMappingURL=app.module.js.map
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TargetsComponent } from './targets/targets.component';
import { ImagesComponent } from './images/images.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
    {
        path: '',
        component: HomeComponent
    },
    {
        path: 'images',
        redirectTo: '/images/next',
        pathMatch: 'full'
    },
    {
        path: 'images/:id',
        component: ImagesComponent
    },
    {
        path: 'targets',
        component: TargetsComponent
    }
];

@NgModule({
    imports: [RouterModule.forRoot(
        routes,
        // For debugging only
        // { enableTracing: true }
    )],
    exports: [RouterModule]
})
export class AppRoutingModule { }

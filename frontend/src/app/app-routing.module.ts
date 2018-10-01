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
        component: ImagesComponent
    },
    {
        path: 'targets',
        component: TargetsComponent
    }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

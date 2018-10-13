import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TargetsComponent } from './targets/targets.component';
import { ImagesComponent } from './images/images.component';
import { HomeComponent } from './home/home.component';
import { TargetClassifierComponent } from './images/target-classifier/target-classifier.component';

@NgModule({
  declarations: [
    AppComponent,
    ImagesComponent,
    TargetsComponent,
    HomeComponent,
    TargetClassifierComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule }   from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TargetsComponent } from './targets/targets.component';
import { ImagesComponent } from './images/images.component';
import { HomeComponent } from './home/home.component';
import { TargetClassifierComponent } from './images/target-classifier/target-classifier.component';
import { TargetEditorComponent } from './targets/target-modifers/target-editor/target-editor.component';
import { TargetMergerComponent } from './targets/target-modifers/target-merger/target-merger.component';

@NgModule({
  declarations: [
    AppComponent,
    ImagesComponent,
    TargetsComponent,
    HomeComponent,
    TargetClassifierComponent,
    TargetEditorComponent,
    TargetMergerComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

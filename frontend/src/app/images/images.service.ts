import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from 'environments/environment'

@Injectable({
  providedIn: 'root'
})
export class ImagesService {
  constructor(private http: HttpClient) { }

  getNext() {
    return this.http.get(environment.api_url + "/next");
  }

  getImageURL(image: any) {
    return environment.api_url + image["image"];
  }
}
